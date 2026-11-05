#!/usr/bin/env python3
"""Pin a published GHCR digest in the matching source revision's Compose file."""
import argparse
from pathlib import Path
import re

from validate import validate_image_reference


IMAGE_ANCHOR = re.compile(r"^x-app-image: &app-image\n  image: (\S+)$", re.MULTILINE)


def image_reference(source: str) -> str:
    """Read the single validated reference used by all application roles."""
    matches = IMAGE_ANCHOR.findall(source)
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one x-app-image anchor")
    validate_image_reference(matches[0])
    return matches[0]


def pin(source: str, image: str) -> str:
    validate_image_reference(image)
    updated, count = IMAGE_ANCHOR.subn("x-app-image: &app-image\n  image: " + image, source)
    if count != 1:
        raise RuntimeError("Expected exactly one x-app-image anchor")
    return updated


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="Complete ghcr.io/owner/repository@sha256:… reference")
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / "compose.yaml"
    path.write_text(pin(path.read_text(), args.image))
    print("Pinned the published image in compose.yaml. Validate and smoke-test before deployment.")
