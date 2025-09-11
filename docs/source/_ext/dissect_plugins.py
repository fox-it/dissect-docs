from __future__ import annotations

import textwrap
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dissect.target.exceptions import PluginError
from dissect.target.helpers import docs
from dissect.target.plugin import load, plugins
from sphinx.application import Sphinx
from sphinx.util.console import colorize
from sphinx.util.display import status_iterator
from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from flow.record import RecordDescriptor

LOGGER = getLogger(__name__)

PAGE_TEMPLATE = """..
    generated, remove this comment to keep this file

{title}

.. code-block:: console

    $ target-query <path/to/target> -f {name}

{variants}
"""

VARIANT_TEMPLATE = """
.. list-table::
    :widths: 20 80

    * - Module
      - ``{module}.{class}``
    * - Output
      - ``{output}``
    * - Source
      - {source}

Module documentation
--------------------

{class_doc}

Function documentation
----------------------

{func_doc}

Record output
-------------

{record_doc}
"""

NAMESPACE_TEMPLATE = """
This is a namespace plugin. This means that by running this plugin, it will automatically run
all other plugins under this namespace:

.. toctree::
    :maxdepth: 1
    :glob:

{exports}
"""

INDEX_TEMPLATE = """\
Plugin Reference
================

.. toctree::
    :maxdepth: 1
    :glob:

    /plugins/*/index
    /plugins/*
"""

def builder_inited(app: Sphinx) -> None:
    dst = Path(app.srcdir).joinpath("plugins")
    if not dst.exists():
        dst.mkdir()

    plugin_map = {}

    for plugin in plugins():
        # Ignore all modules in general as those are all internal or utility
        if plugin.path.startswith("general."):
            continue

        # # Exclude plugins without any exports and/or InternalPlugins
        # if not plugin.findable or not plugin.exports:
        #     continue

        if ns := plugin.namespace:
            plugin_map.setdefault(ns, []).append(plugin)

        for export in plugin.exports:
            if export == "__call__":
                continue

            if ns:
                export = f"{ns}.{export}"
            plugin_map.setdefault(export, []).append(plugin)

    dst.joinpath("index.rst").write_text(INDEX_TEMPLATE)

    for name, plugin in status_iterator(
        plugin_map.items(),
        colorize("bold", "[Dissect] Writing plugin files... "),
        length=len(plugin_map),
        stringify_func=(lambda x: x[0]),
    ):

        if name == plugin[0].namespace:
            dst_path = dst.joinpath(f"{name.replace('.', '/')}/index.rst")
        else:
            dst_path = dst.joinpath(name.replace(".", "/") + ".rst")

        if not dst_path.parent.is_dir():
            dst_path.parent.mkdir()

        dst_path.write_text(_format_template(app, name, plugin))


def build_finished(app: Sphinx, exception: Exception) -> None:
    if not app.config.dissect_plugins_keep_files:
        dst = Path(app.srcdir).joinpath("plugins")
        if app.verbosity > 1:
            LOGGER.info(colorize("bold", "[Dissect] ") + colorize("darkgreen", "Cleaning generated .rst files"))

        for rst in dst.glob("**.rst"):
            with rst.open("rb") as fh:
                if fh.read(16) != b"..\n    generated":
                    continue
            rst.unlink()


def _format_template(app: Sphinx, name: str, plugins: list[dict]) -> str:
    func_name = name.split(".")[-1] if "." in name else name
    variants = []

    for plugin in plugins:
        try:
            plugin_class = load(plugin)
        except PluginError as e:
            LOGGER.warning(
                colorize("bold", "[Dissect] ") + colorize("darkred", f"Error loading plugin {plugin.module}: {e}")
            )
            continue

        class_doc = docs.get_docstring(plugin_class)

        if (ns := plugin.namespace) and name == ns:
            func_output = "records"
            func_doc = NAMESPACE_TEMPLATE.format(
                exports="\n".join(
                    f"    /plugins/{ns.replace('.', '/')}/{export}.rst" for export in plugin.exports if export != "__call__"
                )
            )
            record_doc = get_record_docs(plugin.cls.__record_descriptors__) if hasattr(plugin.cls, "__record_descriptors__") else ""
        else:
            func = getattr(plugin_class, func_name)
            func_output, func_doc = docs._get_func_details(func)
            record_doc = get_record_docs(func.__record__) if hasattr(func, "__record__") else "This plugin does not generate record output."

        info = {
            "module": plugin.module,
            "class": plugin.qualname,
            "output": func_output,
            "class_doc": class_doc,
            "func_doc": func_doc,
            "record_doc": record_doc,
            "source": f"{app.config.dissect_source_base_url}/{plugin.module.replace('.', '/')}.py",
        }

        variants.append(VARIANT_TEMPLATE.format(**info))

    return PAGE_TEMPLATE.format(
        title=f"``{name}``\n{(len(name) + 4) * '='}",
        name=name,
        variants="\n\n".join(variants),
    )


def get_record_docs(records: list[RecordDescriptor] | RecordDescriptor) -> str:
    """Generate a rst list table based on :class:`RecordDescriptor` fields."""

    output = []
    records = records if isinstance(records, list) else [records]
    for desc in records:
        if not desc:
            continue

        out = f"""

        {desc.name}
        {"~"*len(desc.name)}

        .. list-table::
            :widths: 20 20 60
            :header-rows: 1

            * - Field name
              - Field type
              - Description\n"""

        for field in desc.fields.values():
            out += f"            * - ``{field.name}``\n              - ``{field.typename}``\n              - \n"

        output.append(textwrap.dedent(out))

    return "\n\n".join(["This plugin can output the following records.", *output] if output else [*output])


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", builder_inited)
    app.connect("build-finished", build_finished)
    app.add_config_value("dissect_plugins_keep_files", False, "html")
    app.add_config_value("dissect_source_base_url", "https://github.com/fox-it/dissect.target/tree/main", "html")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
