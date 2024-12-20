# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "D'Hondt Calculation System"
copyright = "2024, Esteban Faye"
author = "Esteban Faye"

# The short X.Y version
version = "v0.2.2"
# The full version, including alpha/beta/rc tags
release = ""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.programoutput",
    "m2r",
    "sphinx_autodoc_typehints",  # For type hint documentation
    'sphinx_sqlalchemy',
    "sphinxcontrib.redoc",
]

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = [".rst", ".md"]
master_doc = "index"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_theme_options = {
    "display_version": True,
}

htmlhelp_basename = "DHondtdoc"


# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Redoc configuration ---------------------------------------------------
redoc_uri = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
redoc = [
    {
        "name": "D'Hondt API",
        "page": "api",
        "spec": "_static/dhondt.yaml",
        "embed": True,
    },
]
