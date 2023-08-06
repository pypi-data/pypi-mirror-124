#!/usr/bin/env python3

# External dependencies.
import markdown


class Extension(markdown.extensions.Extension):
    md: markdown.core.Markdown

    def extendMarkdown(self, md: markdown.core.Markdown) -> None:
        self.md = md
        md.registerExtension(self)

    def reset(self) -> None:
        # Markdown has an extension that uses the `Meta` attribute.
        self.md.Meta = {}  # type: ignore[attr-defined]
