"""
This extension generates csv files for our supported targets.
"""

from __future__ import annotations

import csv
import importlib
import inspect
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TextIO
from unittest.mock import Mock, patch

from dissect.target.container import Container
from dissect.target.filesystem import Filesystem
from dissect.target.loader import LOADERS_BY_SCHEME, Loader
from dissect.target.plugin import PLUGINS, ChildTargetPlugin, OSPlugin
from dissect.target.volume import EncryptedVolumeSystem, LogicalVolumeSystem, VolumeSystem
from sphinx.util.logging import getLogger
from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType

    from sphinx.application import Sphinx

LOGGER = getLogger(__name__)
ORIG_IMPORT = __import__


@dataclass(eq=True, frozen=True)
class CSVItemBase:
    module: str
    type_: str
    name: str
    description: str

    @classmethod
    def from_class(cls, klass: type, spec: LookupSpec, info: dict[str, str], **kwargs) -> Self:
        _type = getattr(klass, "__type__", klass.__name__.removesuffix(spec.remove_suffix).lower())
        description = info.get(_type, "")

        if not description:
            LOGGER.warning(
                ("There was no description defined for %s. Please add a description for %r inside '_defaults/%s.csv'"),
                klass.__name__,
                _type,
                spec.name,
            )
        return cls(
            module=klass.__module__,
            type_=_type,
            name=klass.__name__,
            description=description,
            **kwargs,
        )

    @property
    def sphinx_class_string(self) -> str:
        return f":class:`~{self.module}.{self.name}`"

    def as_dict(self) -> dict[str, str]:
        return {
            "Class": self.sphinx_class_string,
            "Description": self.description,
        }


class CSVItem(CSVItemBase):
    def as_dict(self) -> dict[str, str]:
        return {
            "Class": self.sphinx_class_string,
            "Type": f"``{self.type_}``",
            "Description": self.description,
        }


@dataclass(eq=True, frozen=True)
class LoaderCSVItem(CSVItemBase):
    shorthand: str = ""

    def as_dict(self) -> dict[str, str]:
        shorthand = self.shorthand
        if self.type_ == "direct":
            shorthand = "--direct"

        return {
            "Class": self.sphinx_class_string,
            "CMD Option": f"``{shorthand}``" if shorthand else "",
            "Description": self.description,
        }


def parse_descriptions(csv_file: Path) -> dict[str, str]:
    target_dict: dict[str, str] = {}
    try:
        with csv_file.open("rt") as defaults:
            file = csv.DictReader(defaults)
            for line in file:
                target_dict.update({line["name"]: line["description"]})
    except FileNotFoundError:
        LOGGER.warning("missing defaults file at '_defaults/%s'", csv_file.name)
        return {}

    return target_dict


def _create_loader_items(spec: LookupSpec, info: dict[str, str]) -> set[CSVItemBase]:
    loader_items: set[LoaderCSVItem] = set()

    with patch("builtins.__import__", side_effect=mocked_import):
        loader_items.update(
            LoaderCSVItem.from_class(klass.realattr, spec=spec, info=info, shorthand=f"-L {shorthand}")
            for (shorthand, klass) in LOADERS_BY_SCHEME.items()
        )
        loaders = importlib.import_module(spec.subclass_location)

        loader_items.update(
            LoaderCSVItem.from_class(klass, spec=spec, info=info) for klass in _find_subclasses(loaders, spec)
        )

    return loader_items


def _create_os_items(spec: LookupSpec, info: dict[str, str]) -> set[CSVItemBase]:
    operating_systems: set[CSVItemBase] = set()

    for plugin_desc in PLUGINS.__plugins__.__os__.values():
        module = importlib.import_module(plugin_desc.module)
        klass: type = getattr(module, plugin_desc.qualname)
        operating_systems.add(CSVItemBase.from_class(klass, spec=spec, info=info))

    return operating_systems


def _create_items(spec: LookupSpec, info: dict[str, str], item_class: type[CSVItemBase] = CSVItem) -> set[CSVItemBase]:
    base_module = importlib.import_module(spec.subclass_location)
    csv_items: set[CSVItemBase] = set()
    csv_items.update(
        item_class.from_class(class_, spec=spec, info=info) for class_ in _find_subclasses(base_module, spec)
    )

    return csv_items


def _create_partition_items(spec: LookupSpec, info: dict[str, str]) -> set[CSVItemBase]:
    partition_schemes: set[CSVItemBase] = set()

    module = importlib.import_module(spec.subclass_location)
    partition_schemes.update(
        CSVItemBase.from_class(getattr(module, name), spec=spec, info=info) for name in module.__all__
    )

    return partition_schemes


def mocked_import(name: str, *args) -> ModuleType:
    """Mock all the unknown imports"""
    try:
        return ORIG_IMPORT(name, *args)
    except ImportError:
        return Mock()


def _find_subclasses(module: ModuleType, spec: LookupSpec) -> Iterator[type]:
    for path in Path(module.__spec__.origin).parent.iterdir():
        if not path.is_file():
            continue
        if path.stem == "__init__":
            continue

        component = importlib.import_module(".".join([module.__name__, path.stem]))
        yield from _filter_subclasses(spec, component)


def _filter_subclasses(spec: LookupSpec, module: ModuleType) -> Iterator[type]:
    exclusions: list[type] = spec.exclusions

    if callable(exclusions):
        exclusions = exclusions()

    for _, _class in inspect.getmembers(module):
        if not inspect.isclass(_class):
            continue

        if _class is spec.base_class:
            continue

        if _class in exclusions:
            continue

        if issubclass(_class, spec.base_class):
            yield _class


def write_to_csv(output_file: TextIO, items: list[CSVItemBase]) -> None:
    first_item = items[0].as_dict()

    writer = csv.DictWriter(output_file, fieldnames=first_item.keys())
    writer.writeheader()
    writer.writerow(first_item)
    writer.writerows(item.as_dict() for item in items[1:])


@dataclass
class LookupSpec:
    name: str
    base_class: type | None
    remove_suffix: str = ""
    subclass_location: str = ""
    exclusions: list[type] | Callable[[], list[type]] = field(default_factory=list)
    item_function: Callable[[LookupSpec, dict[str, str]], set[CSVItemBase]] = _create_items


def _loader_exclusions() -> list[type[Loader]]:
    return [loader.realattr for loader in LOADERS_BY_SCHEME.values()]


SUPPORTED_SYSTEMS = [
    LookupSpec(
        name="loaders",
        base_class=Loader,
        remove_suffix="Loader",
        subclass_location="dissect.target.loaders",
        exclusions=_loader_exclusions,
        item_function=_create_loader_items,
    ),
    LookupSpec(
        name="volumes",
        base_class=VolumeSystem,
        remove_suffix="VolumeSystem",
        subclass_location="dissect.target.volumes",
        exclusions=[EncryptedVolumeSystem, LogicalVolumeSystem],
    ),
    LookupSpec(
        name="containers",
        base_class=Container,
        remove_suffix="Container",
        subclass_location="dissect.target.containers",
    ),
    LookupSpec(
        name="filesystems",
        base_class=Filesystem,
        remove_suffix="Filesystem",
        subclass_location="dissect.target.filesystems",
    ),
    LookupSpec(
        name="child_targets",
        base_class=ChildTargetPlugin,
        remove_suffix="ChildTargetPlugin",
        subclass_location="dissect.target.plugins.child",
        item_function=partial(_create_items, item_class=CSVItemBase),
    ),
    LookupSpec(name="operating_systems", base_class=OSPlugin, remove_suffix="Plugin", item_function=_create_os_items),
    LookupSpec(
        name="partition_schemes",
        base_class=None,
        subclass_location="dissect.volume.disk.schemes",
        item_function=_create_partition_items,
    ),
]


def builder_inited(app: Sphinx) -> None:
    dst = Path(app.srcdir).joinpath("supported_targets")
    dst.mkdir(exist_ok=True)

    csv_default_dir = Path(app.srcdir).joinpath("_defaults")

    for spec in SUPPORTED_SYSTEMS:
        info_dict = parse_descriptions(csv_default_dir.joinpath(f"{spec.name}.csv"))
        csv_items = list(spec.item_function(spec, info_dict))
        csv_items.sort(key=lambda x: x.name)
        with dst.joinpath(f"{spec.name}.csv").open("wt") as fh:
            write_to_csv(fh, csv_items)


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", builder_inited)
    app.add_config_value("dissect_table_keep_files", False, "html")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
