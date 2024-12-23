# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from sphinx.jinja2glue import BuiltinTemplateLoader

sys.path.insert(0, os.path.abspath('../../'))

project = 'spreadsheet-intelligence'
copyright = 'Galirage, Inc'
author = 'Galirage, Inc.'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
]
autosummary_generate = True

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'show-inheritance': True,
    'member-order': 'bysource',
}


templates_path = ['_templates']
exclude_patterns = []

napoleon_custom_sections = [('XMLReference', 'params_style')]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

def rst_filter(text):
    # テキストをRST形式で返す
    return text or ""

def add_jinja_filters(app):
    env = app.builder.templates.environment
    env.filters['rst'] = rst_filter

def setup(app):
    app.connect('builder-inited', add_jinja_filters)


html_theme = "pydata_sphinx_theme"
# html_static_path = ['_static']

html_title = project

html_theme_options = {
    "navbar_end": ["search-field.html", "theme-switcher", "version-switcher"],
    "show_toc_level": 2,
    "collapse_navigation": False,
    "navigation_depth": 4,
    "show_prev_next": False,
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
}

