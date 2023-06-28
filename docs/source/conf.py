# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())


project = 'westat'
copyright = '2023, westat team'
author = 'westat team'
release = '0.2.2'
version = '0.2.2'
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.autosectionlabel',
    'nbsphinx',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"  # pydata_sphinx_theme press,sphinx_rtd_theme

html_theme_options = {
    'logo_only': True
}
html_show_sourcelink = False
html_static_path = ['_static']
html_logo = '_static/images/logo.png'
html_favicon = '_static/images/logo.png'
html_css_files = [
    'custom.css',
]



# EPUB options
epub_show_urls = 'footnote'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

# ext sphinxcontrib.bibtex options
bibtex_bibfiles = ['refs.bib']
