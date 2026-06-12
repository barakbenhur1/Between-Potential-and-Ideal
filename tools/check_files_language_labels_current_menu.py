#!/usr/bin/env python3
from __future__ import annotations

import re

import check_files_language_labels as audit


# Preserve every existing language-label rule. Only expand the navigation
# exclusion from the legacy anchor switch to the current details menu.
audit.LANGUAGE_SWITCH_RE = re.compile(
    r'(?:'
    r'<a\b(?=[^>]*\bclass\s*=\s*["\'][^"\']*\blanguage-switch\b[^"\']*["\'])[^>]*>.*?</a>'
    r'|'
    r'<details\b(?=[^>]*\bclass\s*=\s*["\'][^"\']*\bbpi-language-menu\b[^"\']*["\'])[^>]*>.*?</details>'
    r')',
    flags=re.I | re.S,
)


if __name__ == "__main__":
    raise SystemExit(audit.main())
