from pathlib import Path
from typing import Any

from dissect.target.exceptions import PluginError
from dissect.target.helpers import docs
from dissect.target.plugin import load, plugins
from sphinx.application import Sphinx
from sphinx.util.console import colorize
from sphinx.util.display import status_iterator
from sphinx.util.logging import getLogger

LOGGER = getLogger(__name__)

PAGE_TEMPLATE = """..
    generated, remove this comment to keep this file

{title}

.. code-block:: console

    $ target-query <path/to/target> -f {name}

{variants}
"""

VARIANT_TEMPLATE = """
.. list-table:: Details
    :widths: 20 80

    * - Module
      - ``{module}.{class}``
    * - Output
      - ``{output}``

**Module documentation**

{class_doc}

**Function documentation**

{func_doc}
"""

NAMESPACE_TEMPLATE = """
This is a namespace plugin. This means that by running this plugin, it will automatically run
all other plugins under this namespace:

{exports}
"""


def builder_inited(app: Sphinx) -> None:
    dst = Path(app.srcdir).joinpath("plugins")
    if not dst.exists():
        dst.mkdir()

    plugin_map = {}
    for plugin in plugins():
        # Ignore all modules in general as those are all internal or utility
        if plugin["module"].startswith("general."):
            continue

        if ns := plugin["namespace"]:
            plugin_map.setdefault(ns, []).append(plugin)

        for export in plugin["exports"]:
            if export == "get_all_records":  # TODO we need to remove this
                continue

            if ns:
                export = f"{ns}.{export}"
            plugin_map.setdefault(export, []).append(plugin)

    for name, plugin in status_iterator(
        plugin_map.items(),
        colorize("bold", "[Dissect] Writing plugin files... "),
        length=len(plugin_map),
        stringify_func=(lambda x: x[0]),
    ):
        dst_path = dst.joinpath(name + ".rst")
        if dst_path.exists():
            continue

        dst_path.write_text(_format_template(name, plugin))


def build_finished(app: Sphinx, exception: Exception) -> None:
    if not app.config.dissect_plugins_keep_files:
        dst = Path(app.srcdir).joinpath("plugins")
        if app.verbosity > 1:
            LOGGER.info(
                colorize("bold", "[Dissect] ")
                + colorize("darkgreen", "Cleaning generated .rst files")
            )

        for rst in dst.glob("*.rst"):
            with open(rst, "rb") as fh:
                if fh.read(16) != b"..\n    generated":
                    continue
            rst.unlink()


def _format_template(name: str, plugins: list[dict]) -> str:
    func_name = name.split(".")[-1] if "." in name else name
    variants = []
    for plugin in plugins:
        try:
            plugin_class = load(plugin)
        except PluginError as e:
            LOGGER.warning(
                colorize("bold", "[Dissect] ")
                + colorize("darkred", f"Error loading plugin {plugin['module']}: {e}")
            )
            continue

        class_doc = docs.get_docstring(plugin_class)

        if (ns := plugin["namespace"]) and name == ns:
            func_output = "records"
            func_doc = NAMESPACE_TEMPLATE.format(
                exports="\n".join(
                    f"- :doc:`/plugins/{ns}.{export}`"
                    for export in plugin["exports"]
                    if export != "get_all_records"
                )
            )
        else:
            func = getattr(plugin_class, func_name)
            func_output, func_doc = docs.get_func_details(func)

        info = {
            "module": plugin["module"],
            "class": plugin["class"],
            "output": func_output,
            "class_doc": class_doc,
            "func_doc": func_doc,
        }

        variants.append(VARIANT_TEMPLATE.format(**info))

    title = f"``{name}``\n{(len(name) + 4) * '='}"
    return PAGE_TEMPLATE.format(
        title=title,
        name=name,
        variants="\n\n".join(variants),
    )


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", builder_inited)
    app.connect("build-finished", build_finished)
    app.add_config_value("dissect_plugins_keep_files", False, "html")

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
