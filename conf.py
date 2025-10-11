# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from http.server import SimpleHTTPRequestHandler
from typing import Any

from docutils import nodes
from docutils.nodes import TextElement
from sphinx.transforms import SphinxTransform
from sphinx.transforms.post_transforms.code import HighlightLanguageTransform

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "Jack Burridge"
copyright = "2025, Jack Burridge"
author = "Jack Burridge"
html_title = "Jack Burridge"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["ablog", "sphinx_copybutton", "sphinx_togglebutton"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", ".venv"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML 'Thumbs.db', '.DS_Store', Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- ABlog ---------------------------------------------------

blog_path = "blog"
blog_post_pattern = "blog/*/*"
blog_feed_fulltext = True
blog_feed_subtitle = "Open communities, open science, communication, and data."
fontawesome_included = True
post_redirect_refresh = 1
post_auto_image = 1
post_auto_excerpt = 2


html_theme_options = {
    "logo": {
        "text": "Jack Burridge",
        "image_light": "_static/logo.jpg",
        "image_dark": "_static/logo.jpg",
    },
    "footer_start": [],
    "footer_end": [],
    "search_bar_text": "Search...",
}


html_css_files = [
    "css/custom.css",
]


html_sidebars = {
    # "index": ["hello.html"],
    # "about": ["hello.html"],
    # "publications": ["hello.html"],
    # "projects": ["hello.html"],
    # "talks": ["hello.html"],
    "blog": ["ablog/categories.html", "ablog/tagcloud.html", "ablog/archives.html"],
    "blog/**": ["ablog/postcard.html", "ablog/recentposts.html", "ablog/archives.html"],
}


html_favicon = "_static/favicon.ico"


class TrimWhitespaceTransform(SphinxTransform):

    default_priority = HighlightLanguageTransform.default_priority + 1

    def apply(self, **kwargs: Any) -> None:
        for lb_node in self.document.findall(nodes.literal_block):
            self.strip_trailing(lb_node)

    @staticmethod
    def strip_trailing(node: TextElement) -> None:
        source = node.rawsource.rstrip().lstrip()
        node.rawsource = source
        node[:] = [nodes.Text(source)]


def setup(app):
    app.add_transform(TrimWhitespaceTransform)

    return {}
