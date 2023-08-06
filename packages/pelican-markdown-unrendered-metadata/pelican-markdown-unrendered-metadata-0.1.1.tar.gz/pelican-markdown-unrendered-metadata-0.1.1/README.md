# Pelican Markdown Unrendered Metadata

Read Pelican metadata from link references.

## Usage

Write metadata in the form `[//Pelican/KEY]: # (VALUE)`.
They can be placed anywhere in the document.
If the first text content is a top-level heading,
the heading is removed from the document, and used as the title.
For example,

```md
# Hello, world!

[//Pelican/date]: # (2000-10-31 00:00)
[//Pelican/author]: # (Noname)

Goodbye, world!
```

The equivalent MultiMarkdown document used by Pelican would be

```md
title: Hello, world!
date: 2000-10-31 00:00
author: Noname

Goodbye, world!
```

If a key has multiple sources (references, MultiMarkdown, heading),
the order of stored value is unspecified.

## Installation

If `PLUGINS` is not specified inside `pelicanconf.py`,
then installing this package should be sufficient setup.

```sh
python -m pip install pelican-markdown-unrendered-metadata
```

Otherwise, inside `pelicanconf.py`,
add `markdown_unrendered_metadata` to the `PLUGINS` list variable.

## Raison d'être

Pelican metadata of Markdown documents
are colon-separated key-value pairs at the beginning of the document.
Markdown parsers see them as a block of text
and generate an unintended paragraph when rendered.

To mitigate this, the metadata can be embedded
inside a form of Markdown comments.
This plugin uses link references as comments, suggested by a
[StackOverflow answer](https://stackoverflow.com/a/20885980):

```md
[//]: # (This may be the most platform independent comment)
```
