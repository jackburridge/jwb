import os
import sys
from typing import Any

from docutils import nodes
from docutils.nodes import TextElement
from sphinx.transforms import SphinxTransform
from sphinx.transforms.post_transforms.code import HighlightLanguageTransform


# -- Path setup --------------------------------------------------------------

sys.path.append(os.path.abspath("_ext"))


# -- Project information -----------------------------------------------------

project = "Jack Burridge"
copyright = "2025, Jack Burridge"
author = "Jack Burridge"
html_title = "Jack Burridge"


# -- General configuration ---------------------------------------------------

extensions = [
    "ablog",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx.ext.intersphinx",
    "readtime",
    "sphinxext.opengraph",
    "sphinx_sitemap",
]

templates_path = ["_templates"]

exclude_patterns = ["_build", ".venv"]


# -- Options for HTML output -------------------------------------------------


html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
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
    "blog": ["ablog/categories.html", "ablog/tagcloud.html", "ablog/archives.html"],
    "blog/**": ["ablog/postcard.html", "ablog/recentposts.html", "ablog/archives.html"],
}
html_favicon = "_static/favicon.ico"
html_baseurl = "https://jackburridge.com/"
html_extra_path = ["robots.txt"]


# -- ABlog ---------------------------------------------------

blog_path = "blog"
blog_post_pattern = "blog/*/*"
blog_feed_fulltext = True
blog_feed_subtitle = "Open communities, open science, communication, and data."
fontawesome_included = True
post_redirect_refresh = 1
post_auto_image = 1
post_auto_excerpt = 2


# -- intersphinx ---------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "locust": ("http://docs.locust.io/en/stable", None),
    "gevent": ("https://www.gevent.org/", None),
}

# -- readtime -----------------------------------------------


readtime_include_patterns = ["blog/*/*"]


# -- OpenGraph config ---------------------------------------

ogp_site_url = "https://jackburridge.com"

# -- sitemap ------------------------------------------------

sitemap_filename = "sitemap-override.xml"
sitemap_url_scheme = "{link}"


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
