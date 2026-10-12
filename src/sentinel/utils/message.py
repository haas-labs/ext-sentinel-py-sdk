"""
Message templates with named placeholders

A template is plain text with `{name}` blanks, e.g. "{node} failed (attempt {attempt}): {error}".
`render_message` fills the blanks it has a value for and leaves every other one as written, so a
template that names a placeholder the caller does not know still renders instead of failing.

The same rules are implemented in sentinel-workflows (it does not depend on the SDK), which files
the workflow step events; keep the two consistent.
"""

import re
from collections.abc import Mapping
from typing import Any

# `{name}` with a word name. Anything else (a lone brace, `{}`, `{a b}`) is plain text.
_PLACEHOLDER = re.compile(r"\{(\w+)\}")


def render_message(template: str | None, values: Mapping[str, Any], default: str = "") -> str:
    """
    Fill the `{name}` placeholders of `template` from `values`

    - a missing, blank or non-string template falls back to `default` (rendered the same way)
    - an unknown placeholder is left as-is, `{name}` included
    - a `None` value renders as an empty string
    - one pass over the template: a value that itself contains `{name}` is not filled again
    """
    text = template if isinstance(template, str) and template.strip() else default

    def fill(match: re.Match) -> str:
        name = match.group(1)
        if name not in values:
            return match.group(0)
        value = values[name]
        return "" if value is None else str(value)

    return _PLACEHOLDER.sub(fill, text)
