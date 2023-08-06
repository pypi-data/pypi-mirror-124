#!/usr/bin/env python3

# External dependencies.
import pelican  # type: ignore[import]

# Internal modules.
from pelican_markdown_unrendered_metadata import (
    markdown_metadata_in_heading as heading_extension,
    markdown_metadata_in_reference as reference_extension,
)


def on_pelican_initialized(pelican_object: pelican.Pelican) -> None:
    markdown_settings = pelican_object.settings["MARKDOWN"]
    markdown_extensions = markdown_settings.setdefault("extensions", [])
    markdown_extensions.append(heading_extension.__name__)
    markdown_extensions.append(reference_extension.__name__)


# Pelican namespace plugin interface.
def register() -> None:
    pelican.signals.initialized.connect(on_pelican_initialized)
