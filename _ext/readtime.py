import math
import re
from typing import Any
from typing import Optional

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.matching import patmatch


def has_read_time(node: nodes.Node) -> bool:

    for paragraph in node.findall(nodes.paragraph):
        if "read-time" in paragraph["classes"]:
            return True
    return False


def find_title(node: nodes.Node) -> Optional[nodes.title]:
    for title in node.findall(nodes.title):
        return title
    return None


WORD_PATTERN = re.compile(r"[A-Z]+[a-z]*|[a-z]+|\d+")


class AddReadTime(SphinxTransform):
    default_priority = 200

    def apply(self, **kwargs: Any) -> None:

        docname = self.env.path2doc(self.document["source"])
        if docname is None:
            return

        exclude = any(
            [patmatch(docname, p) for p in self.config.readtime_exclude_patterns]
        )
        include = not exclude and any(
            [patmatch(docname, p) for p in self.config.readtime_include_patterns]
        )
        if include and not has_read_time(self.document):
            title = find_title(self.document)
            if title is not None:
                title_index = title.parent.index(title)

                words = WORD_PATTERN.findall(self.document.astext())
                read_time = math.ceil(
                    len(words) / self.config.readtime_average_words_per_minute
                )

                paragraph = nodes.paragraph("", nodes.Text(f"{read_time} min read"))

                paragraph["classes"] = ["readtime"]
                title.parent.insert(title_index + 1, paragraph)


def setup(app):
    app.add_config_value("readtime_include_patterns", [], "env")
    app.add_config_value("readtime_exclude_patterns", [], "env")
    app.add_config_value("readtime_average_words_per_minute", 265, True)

    app.add_transform(AddReadTime)

    return {}
