from pathlib import Path
from typing import Any
from typing_extensions import override

from sphinx.application import Sphinx
from sphinx.util.logging import getLogger
from sphinx.addnodes import pending_xref
from docutils.parsers.rst.directives.tables import ListTable
from docutils.parsers.rst import directives
from docutils import nodes


LOGGER = getLogger(__name__)


class SupportedTargetTable(ListTable):
    """Extended list-table directive that validates if we have all our supported target modules documented."""

    option_spec = ListTable.option_spec.copy()
    option_spec["submodule-path"] = directives.unchanged_required
    option_spec["blacklist"] = directives.unchanged
    option_spec["glob-pattern"] = directives.unchanged

    @override
    def run(self):
        # Call the parent directive to get the table node
        result = super().run()

        module_references = []
        table_name = ""
        # Perform custom checks on the table
        if result and isinstance(result[0], nodes.table):
            table_node = result[0]
            table_name = table_node[0].astext()
            LOGGER.info("Gathering references from table '%s'", table_name)
            module_references = self._gather_table_references(table_node)

        if module_references:
            self.validate_references(table_name, module_references)

        return result

    def _gather_table_references(self, table_node: nodes.table) -> list[str]:
        """Gather all the references inside the table."""
        references = []
        for ref in table_node.findall(pending_xref):
            target = ref.get("reftarget")
            split_names = target.rsplit(".", 2)
            if target.endswith("._os"):
                modname = split_names[-2]
            else:
                modname = split_names[-1]
            references.append(modname)

        return references

    def validate_references(self, table_name: str, module_references: list[str]):
        LOGGER.info("Validating module references from table '%s'", table_name)
        check_path: str = self.options.get("submodule-path")
        root = Path(__file__).parent.parent.parent.parent

        submodule_dir = root / "submodules"
        search_path = submodule_dir / check_path

        black_list = set()
        black_list.update(["__init__"])
        black_list.update(
            module for module in self.options.get("blacklist", "").split(",") if module
        )

        glob = self.options.get("glob-pattern", "*.py")
        for file in search_path.glob(glob):
            if file.name == "_os.py":
                file = file.parent

            relative_file = file.relative_to(submodule_dir)

            if file.stem in black_list:
                LOGGER.debug("Skipping %s", relative_file)
                continue
            if file.stem not in module_references:
                LOGGER.warning(
                    "Missing documentation entry for %s in table '%s'",
                    relative_file,
                    table_name,
                )

        LOGGER.info("Done validating table '%s'", table_name)


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_directive("supported-table", SupportedTargetTable)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
