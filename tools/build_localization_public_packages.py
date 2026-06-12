#!/usr/bin/env python3
"""Regenerate all localized public document formats from the sanitized source assembly."""

from __future__ import annotations

import a as D
import build_localization_beta as B


_original_strip_front_matter = B.strip_front_matter


def strip_front_matter_and_controls(text, path):
    return D.clean(_original_strip_front_matter(text, path))


B.strip_front_matter = strip_front_matter_and_controls
B.strip_review_gate = D.clean


if __name__ == "__main__":
    raise SystemExit(B.main())
