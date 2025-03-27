# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("./contributing"))

for path in map(str, Path("../../submodules/").resolve().iterdir()):
    sys.path.insert(0, path)

sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------

project = "Dissect"
copyright = "2023, Fox-IT part of NCC Group"
author = "Fox-IT part of NCC Group"

# The full version, including alpha/beta/rc tags
try:
    release = subprocess.run(["git", "describe", "--tags"], check=True, stdout=subprocess.PIPE).stdout.decode().strip()
except Exception:
    release = "0.0-dev"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx_argparse_cli",
    "sphinx_copybutton",
    "sphinx_design",
    "dissect_plugins",
]

# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True

exclude_patterns = []
# Allow disabling of time consuming autoapi generation
if os.getenv("NO_AUTOAPI"):
    exclude_patterns.append("api/acquire/index")
    api_dir = Path(__file__).parent / "api"

    for dir_name in ["acquire/nop", "dissect/nop", "flow/nop"]:
        api_dir.joinpath(dir_name).mkdir(parents=True)
        api_dir.joinpath(dir_name, "index.rst").write_text(":orphan:\n\nTITLE\n#####\n")

else:
    extensions.append("autoapi.extension")

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

html_favicon = "_static/favicon.svg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
    "css/konami.css",
]

html_js_files = [
    "js/konami.js",
]

html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "css/icons/logo-dark.svg",
    "dark_logo": "css/icons/logo-dark.svg",
    "light_css_variables": {
        "icon-search": 'url(\'data:image/svg+xml;charset=utf-8,<svg width="18" height="18" viewBox="0 0 18 18" stroke="currentColor" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.9778 15.0469L12.2091 11.2781C13.0247 10.2797 13.4747 9.02249 13.4747 7.64999C13.4747 4.41843 10.8554 1.79999 7.62469 1.79999C4.39396 1.79999 1.79999 4.41927 1.79999 7.64999C1.79999 10.8807 4.419 13.5 7.62469 13.5C8.99691 13.5 10.2558 13.0244 11.2528 12.2332L15.0216 16.002C15.1791 16.1353 15.3534 16.2 15.525 16.2C15.6966 16.2 15.8704 16.1341 16.0023 16.0022C16.2647 15.7387 16.2647 15.3112 15.9778 15.0469ZM3.14999 7.64999C3.14999 5.1688 5.16881 3.14999 7.65 3.14999C10.1312 3.14999 12.15 5.1688 12.15 7.64999C12.15 10.1312 10.1312 12.15 7.65 12.15C5.16881 12.15 3.14999 10.1306 3.14999 7.64999Z"/></svg>\')',
        "color-brand-primary": "#1F65AB",
        "color-brand-content": "var(--color-brand-primary)",
        "color-background-hover": "#3574B3",
        "color-background-hover--transparent": "var(--color-background-hover)",
        "color-api-background": "var(--color-background-secondary)",
        "color-api-background-hover": "#EFEFF4FF",
        "color-sidebar-background": "var(--color-brand-primary)",
        "color-sidebar-background-border": "var(--color-background-hover)",
        "color-sidebar-caption-text": "#F3F4F8",
        "color-sidebar-link-text": "#E9ECF2",
        "color-sidebar-link-text--top-level": "#FFFFFF",
        "color-sidebar-search-text": "#6B7386",
        "color-sidebar-search-background": "#F3F4F8",
        "color-sidebar-search-border": "var(--color-background-border)",
        "color-sidebar-search-icon": "#81868D",
    },
    "dark_css_variables": {
        "icon-search": 'url(\'data:image/svg+xml;charset=utf-8,<svg width="18" height="18" viewBox="0 0 18 18" stroke="currentColor" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.9778 15.0469L12.2091 11.2781C13.0247 10.2797 13.4747 9.02249 13.4747 7.64999C13.4747 4.41843 10.8554 1.79999 7.62469 1.79999C4.39396 1.79999 1.79999 4.41927 1.79999 7.64999C1.79999 10.8807 4.419 13.5 7.62469 13.5C8.99691 13.5 10.2558 13.0244 11.2528 12.2332L15.0216 16.002C15.1791 16.1353 15.3534 16.2 15.525 16.2C15.6966 16.2 15.8704 16.1341 16.0023 16.0022C16.2647 15.7387 16.2647 15.3112 15.9778 15.0469ZM3.14999 7.64999C3.14999 5.1688 5.16881 3.14999 7.65 3.14999C10.1312 3.14999 12.15 5.1688 12.15 7.64999C12.15 10.1312 10.1312 12.15 7.65 12.15C5.16881 12.15 3.14999 10.1306 3.14999 7.64999Z"/></svg>\')',
        "color-sidebar-background": "var(--color-background-secondary)",
        "color-sidebar-caption-text": "var(--color-foreground-muted)",
        "color-sidebar-link-text": "var(--color-foreground-secondary)",
        "color-sidebar-link-text--top-level": "var(--color-brand-primary)",
        "color-sidebar-search-text": "var(--color-foreground-primary)",
        "color-sidebar-search-background": "#202020",
        "color-sidebar-search-background--focus": "var(--color-background-primary)",
        "color-sidebar-search-border": "var(--color-background-border)",
        "color-sidebar-search-icon": "var(--color-foreground-muted)",
    },
}

dissect_paths = [path / "dissect" for path in Path("../../submodules/").glob("dissect.*")]
flow_paths = [path / "flow" for path in Path("../../submodules/").glob("flow.*")]
acquire_path = Path("../../submodules/acquire")

autoapi_type = "python"
autoapi_dirs = [acquire_path] + dissect_paths + flow_paths
autoapi_ignore = ["*tests*", "*.tox*", "*venv*", "*examples*", "*setup.py"]
autoapi_python_use_implicit_namespaces = True
autoapi_add_toctree_entry = False
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_keep_files = True
autoapi_template_dir = "_templates/autoapi"

autodoc_typehints = "signature"
autodoc_member_order = "groupwise"

autosectionlabel_prefix_document = True

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"
copybutton_here_doc_delimiter = "EOT"
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"
copybutton_exclude = ".linenos"

suppress_warnings = [
    # https://github.com/readthedocs/sphinx-autoapi/issues/285
    "autoapi.python_import_resolution",
    # https://github.com/sphinx-doc/sphinx/issues/4961
    "ref.python",
]
