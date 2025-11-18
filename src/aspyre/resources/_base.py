#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from __future__ import annotations
from enum import Enum
from typing import Any, Iterable, Tuple, TypedDict

from ._models import IconVariant
from .._utils import to_pascal_case

class _ResourceOptions(TypedDict, total=False):
    url: str | Tuple[str, str]
    """Adds a URL to be displayed for the resource. Either url string, or tuple of (url, display_text)."""
    exclude_from_manifest: bool
    """Excludes this resource from being published to the manifest."""
    exclude_from_mcp: bool
    """Excludes the resource from MCP operations using the Aspire MCP server."""
    explicit_start: bool
    """Prevents the resource from being automatically started when the application host starts."""
    health_check: str
    """Adds a health check to the resource."""
    relationship: Resource | Iterable[Resource]
    """Adds a relationship reference to the resource."""
    parent_relationship: Resource | Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    child_relationship: Resource | Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    icon_name: str | Tuple[str, IconVariant]
    """Specifies the icon to use when displaying the resource in the dashboard. Either icon name string,
    or tuple of (icon_name, icon_variant). The default icon variant is Filled."""


class Resource:
    parent: Resource | None = None

    @property
    def package(self) -> str:
        raise NotImplementedError()

    @property
    def _resource(self) -> str:
        raise NotImplementedError()

    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self._options = kwargs

    def _build_value(self, value: Any) -> str:
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, Resource):
            return value.name
        elif isinstance(value, Enum):
            return f"{value.__class__.__name__}.{value.name.title()}"
        else:
            return str(value)

    def _build(self) -> str:
        csharp = ""
        for key, value in self._options.items():
            if value is True:
                csharp += f'\n    .{to_pascal_case(key)}()'
            if isinstance(value, str):
                # Special case str to avoid Iterable handling
                csharp += f'\n    .With{to_pascal_case(key)}("{value}")'
            elif isinstance(value, tuple):
                args = ", ".join([self._build_value(v) for v in value])
                csharp += f'\n    .With{to_pascal_case(key)}({args})'
            elif isinstance(value, Iterable):
                # TODO: Check whether we should support tuple cases here.
                for item in value:
                    csharp += f'\n    .With{to_pascal_case(key)}({self._build_value(item)})'
            else:
                csharp += f'\n    .With{to_pascal_case(key)}({self._build_value(value)})'
        return csharp


class _ResourceWithArgsOptions(TypedDict, total=False):
    ...


class _ResourceWithEndpointsOptions(TypedDict, total=False):
    ...


class _ResourceWithEnvironmentOptions(TypedDict, total=False):
    ...


class _ResourceWithWaitSupportOptions(TypedDict, total=False):
    ...



class ExecutableResourceOptions(_ResourceOptions, _ResourceWithArgsOptions, _ResourceWithEnvironmentOptions, _ResourceWithWaitSupportOptions, _ResourceWithEndpointsOptions, total=False):
    ...


class ExecutableResource(Resource):
    def __init__(self, name: str, **kwargs: ExecutableResourceOptions) -> None:
        super().__init__(name, **kwargs)