#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from dataclasses import dataclass
from contextlib import contextmanager
from io import StringIO
from typing import Any, Mapping, cast, get_origin, get_args, get_type_hints, Annotated
import warnings


@dataclass
class Warnings:
    experimental: str | None


class AspyreExperimentalWarning(Warning):
    """Custom warning for experimental features in Aspire."""


@contextmanager
def experimental(builder: StringIO, arg_name: str, func_or_cls: str | type, code: str):
    if isinstance(func_or_cls, str):
        warnings.warn(
            f"The '{arg_name}' option in '{func_or_cls}' is for evaluation purposes only and is subject "
            f"to change or removal in future updates. (Code: {code})",
            category=AspyreExperimentalWarning,
        )
        builder.write(f"\n#pragma warning disable {code}")
        yield
        builder.write(f"\n#pragma warning restore {code}")
    else:
        warnings.warn(
            f"The '{arg_name}' method of '{func_or_cls.__name__}' is for evaluation purposes only and is subject "
            f"to change or removal in future updates. (Code: {code})",
            category=AspyreExperimentalWarning,
        )
        builder.write(f"\n#pragma warning disable {code}")
        yield
        builder.write(f"\n#pragma warning restore {code}")


@contextmanager
def check_warnings(builder: StringIO, kwargs: Mapping[str, Any], annotations: Any, func_name: str):
    type_hints = get_type_hints(annotations, include_extras=True)
    for key in kwargs.keys():
        if get_origin(type_hint := type_hints.get(key)) is Annotated:
            annotated_warnings = cast(Warnings, get_args(type_hint)[1])
            if annotated_warnings.experimental:
                warnings.warn(
                    f"The '{key}' option in '{func_name}' is for evaluation purposes only and is subject to change"
                    f"or removal in future updates. (Code: {annotated_warnings.experimental})",
                    category=AspyreExperimentalWarning,
                )
                builder.write(f"\n#pragma warning disable {annotated_warnings.experimental}")
                yield
                builder.write(f"\n#pragma warning restore {annotated_warnings.experimental}")
                return
    yield
