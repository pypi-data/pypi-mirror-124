#!/usr/bin/env python3

# Standard libraries.
from __future__ import annotations
import typing

# External dependencies.
import markdown.postprocessors
from . import markdown_metadata


def is_meta_reference(
    key: str, value: tuple[str, str | None], prefix: str
) -> bool:
    return (
        key.startswith(prefix)
        and len(key) > len(prefix)
        and len(value) == 2
        and value[0] == "#"
        and value[1] is not None
    )


class ReferenceMetaProcessor(markdown.postprocessors.Postprocessor):
    def run(self, text: str) -> str:
        md = self.md
        references = md.references
        prefix = "//pelican/"
        meta_references = {
            key: value
            for key, value in references.items()
            if is_meta_reference(key, value, prefix)
        }
        for key in meta_references:
            references.pop(key)
        meta = md.Meta
        for key, value in meta_references.items():
            meta_key = key[len(prefix) :]
            meta.setdefault(meta_key, []).append(value[-1])
        return text


class Extension(markdown_metadata.Extension):
    def extendMarkdown(self, md: markdown.core.Markdown) -> None:
        super().extendMarkdown(md)
        md.postprocessors.register(
            ReferenceMetaProcessor(md), "reference_meta", 30
        )


def makeExtension(
    **kwargs: typing.Any,
) -> Extension:
    return Extension(**kwargs)
