#!/usr/bin/env python3

# Standard libraries.
import typing
import xml.etree.ElementTree

# External dependencies.
import markdown.treeprocessors
from . import markdown_metadata


class HeadingMetaProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, root: xml.etree.ElementTree.Element) -> None:
        # The markdown module not call without children in `root`.
        # So no need to handle `IndexError`.
        first_element = root[0]
        if first_element.tag != "h1":
            return
        md = self.md
        meta = md.Meta
        meta.setdefault("title", []).append(
            "".join(first_element.itertext())
        )
        root.remove(first_element)


class Extension(markdown_metadata.Extension):
    def extendMarkdown(self, md: markdown.core.Markdown) -> None:
        super().extendMarkdown(md)
        md.treeprocessors.register(
            HeadingMetaProcessor(md), "title_meta", 30
        )


def makeExtension(
    **kwargs: typing.Any,
) -> Extension:
    return Extension(**kwargs)
