#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

import re
from enum import Enum
from typing import Any, Iterable, Mapping
from base64 import b64encode

VALID_NAME = re.compile(r'^[a-zA-Z0-9-]+$')

def valid_var_name(name: str) -> str:
    if not VALID_NAME.match(name):
        raise ValueError(f"Invalid name '{name}'. Only alphanumeric characters and hyphens are allowed.")
    return name.replace("-", "_")


def format_string(value: Any) -> str:
    return f'"{value}"'


def format_string_array(strings: Iterable[str] | None) -> str:
    if strings is None:
        return "null"
    formatted_items = ', '.join(format_string(s) for s in strings)
    return f'new string[] {{ {formatted_items} }}'


def format_byte_array(bytes_value: bytes) -> str:
    base64_str = b64encode(bytes_value).decode('utf-8')
    return f'Convert.FromBase64String("{base64_str}")'


def format_enum(enum: Enum) -> str:
    return f'{enum.__class__.__name__}.{enum.value}'


def format_bool(value: bool) -> str:
    if value is None:
        return "null"
    return str(value).lower()


def get_nullable_value(value: Any, default: Any = None) -> str | int:
    if value is None:
        if default is not None:
            return get_nullable_value(default)
        return "null"
    if isinstance(value, Enum):
        return format_enum(value)
    if value in [True, False]:
        return format_bool(value)
    if isinstance(value, int):
        return value
    return format_string(value)


def get_nullable_from_map(value: Mapping[str, Any], key: str, default: Any = None) -> str | int:
    return get_nullable_value(value.get(key), default)


def get_nullable_from_tuple(value: tuple, index: int, default: Any = None) -> str | int:
    if index < len(value):
        return get_nullable_value(value[index], default)
    return get_nullable_value(None, default)
