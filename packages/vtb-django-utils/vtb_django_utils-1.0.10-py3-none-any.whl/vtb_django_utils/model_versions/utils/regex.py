import re


def version_regex(version: str):
    regex = r'^'
    parts = version.split('.')
    for i, part in enumerate(parts):
        if not part:
            continue
        regex += rf'{re.escape(part)}'
        regex += '.?' if i == 2 else r'\.'
    return regex
