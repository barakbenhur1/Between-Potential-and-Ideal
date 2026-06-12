#!/usr/bin/env python3
"""Regenerate all localized public document formats from the sanitized source assembly."""

from __future__ import annotations

import a as D
import build_localization_beta as B


_original_strip_front_matter = B.strip_front_matter
_original_assemble = B.assemble


def strip_front_matter_and_controls(text, path):
    return D.clean(_original_strip_front_matter(text, path))


def assemble_public_package(language, contract):
    text = _original_assemble(language, contract)
    text = text.replace("../../../figures/", "../../figures/")
    return text.replace(
        "v25_chapter-boundary-horizons.png",
        "v25_chapter_boundary-horizons.png",
    )


B.strip_front_matter = strip_front_matter_and_controls
B.strip_review_gate = D.clean
B.assemble = assemble_public_package


if __name__ == "__main__":
    raise SystemExit(B.main())
