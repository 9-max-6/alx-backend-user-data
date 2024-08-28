#!/usr/bin/env python3
"""module: function: filter_datum"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """
    A function to obfuscate a log message
    steps:
    1. split all with ;
    2. list comprehension to replace matched pattern
    3. Join again with the separator
    4. Return
    """
    ps = message.split(separator)
    pattern = "|".join(re.escape(field) + r'=(.*)' for field in fields)
    ob_parts = [re.sub(pattern, (
        lambda match: match.group(0).split("=")[0]+"="+f"{redaction}"
        ), p) for p in ps]
    return separator.join(ob_parts)
