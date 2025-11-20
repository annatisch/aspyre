#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from __future__ import annotations
from typing import Iterable, Literal, TypedDict, MutableSequence

from ._models import IconVariant


class _ResourceOptions(TypedDict, total=False):
    url: str | tuple[str, str]
    """Adds a URL to be displayed for the resource. Either url string, or tuple of (url, display_text)."""
    exclude_from_manifest: Literal[True]
    """Excludes this resource from being published to the manifest."""
    exclude_from_mcp: Literal[True]
    """Excludes the resource from MCP operations using the Aspire MCP server."""
    explicit_start: Literal[True]
    """Prevents the resource from being automatically started when the application host starts."""
    health_check: str
    """Adds a health check to the resource."""
    relationships: tuple[Resource, str] | Iterable[tuple[Resource, str]]
    """Adds a relationship reference to the resource."""
    reference_relationships: Resource | Iterable[Resource]
    """Adds a reference relationship reference to the resource."""
    parent_relationships: Resource | Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    child_relationships: Resource | Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    icon_name: str | tuple[str, IconVariant]
    """Specifies the icon to use when displaying the resource in the dashboard. Either icon name string,
    or tuple of (icon_name, icon_variant). The default icon variant is Filled."""


class Resource:

    @property
    def package(self) -> str:
        raise NotImplementedError()

    @property
    def url(self) -> str | tuple[str, str] | None:
        return self._url

    @url.setter
    def url(self, value: str | tuple[str, str]) -> None:
        if isinstance(value, str):
            self._builder += f"\n{self.name}.WithUrl(\"{value}\");"
        else:
            self._builder += f"\n{self.name}.WithUrl(\"{value[0]}\", \"{value[1]}\");"
        self._url = value

    @property
    def exclude_from_manifest(self) -> bool | None:
        return self._exclude_from_manifest

    @exclude_from_manifest.setter
    def exclude_from_manifest(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.ExcludeFromManifest();"
        self._exclude_from_manifest = value

    @property
    def exclude_from_mcp(self) -> bool | None:
        return self._exclude_from_mcp

    @exclude_from_mcp.setter
    def exclude_from_mcp(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.ExcludeFromMcp();"
        self._exclude_from_mcp = value

    @property
    def explicit_start(self) -> bool | None:
        return self._explicit_start

    @explicit_start.setter
    def explicit_start(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.WithExplicitStart();"
        self._explicit_start = value

    @property
    def health_check(self) -> str | None:
        return self._health_check

    @health_check.setter
    def health_check(self, value: str) -> None:
        self._builder += f'\n{self.name}.WithHealthCheck("{value}");'
        self._health_check = value

    @property
    def relationships(self) -> Iterable[tuple[Resource, str]]:
        return self._relationships

    @relationships.setter
    def relationships(self, value: tuple[Resource, str] | Iterable[tuple[Resource, str]]) -> None:
        if isinstance(value, tuple):
            self._relationships = [value]
            self._builder += f'\n{self.name}.WithRelationship({value[0].name}, "{value[1]}");'
        else:
            self._relationships = []
            for rel in value:
                self._relationships.append(rel)
                self._builder += f'\n{self.name}.WithRelationship({rel[0].name}, "{rel[1]}");'

    @property
    def reference_relationships(self) -> Iterable[Resource]:
        return self._reference_relationships

    @reference_relationships.setter
    def reference_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._reference_relationships = [value]
            self._builder += f'\n{self.name}.WithReferenceRelationship({value.name});'
        else:
            self._reference_relationships = []
            for reference in value:
                self._reference_relationships.append(reference)
                self._builder += f'\n{self.name}.WithReferenceRelationship({reference.name});'

    @property
    def parent_relationships(self) -> Iterable[Resource]:
        return self._parent_relationships

    @parent_relationships.setter
    def parent_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._parent_relationships = [value]
            self._builder += f'\n{self.name}.WithParentRelationship({value.name});'
        else:
            self._parent_relationships = []
            for parent in value:
                self._parent_relationships.append(parent)
                self._builder += f'\n{self.name}.WithParentRelationship({parent.name});'

    @property
    def child_relationships(self) -> Iterable[Resource]:
        return self._child_relationships

    @child_relationships.setter
    def child_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._child_relationships = [value]
            self._builder += f'\n{self.name}.WithChildRelationship({value.name});'
        else:
            self._child_relationships = []
            for child in value:
                self._child_relationships.append(child)
                self._builder += f'\n{self.name}.WithChildRelationship({child.name});'

    @property
    def icon_name(self) -> str | tuple[str, IconVariant] | None:
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value: str | tuple[str, IconVariant]) -> None:
        if isinstance(value, str):
            self._builder += f'\n{self.name}.WithIconName("{value}");'
        else:
            self._builder += f'\n{self.name}.WithIconName("{value[0]}", IconVariant.{value[1].value});'
        self._icon_name = value

    def __init__(self, name: str, builder: str, **kwargs) -> None:
        self.name = name
        self._builder = builder

        self._url = kwargs.pop("url", None)
        if self._url:
            for url in self._url:
                if isinstance(url, str):
                    self._builder += "\n    .WithUrl(\"{}\")".format(url)
                else:
                    self._builder += "\n    .WithUrl(\"{}\", \"{}\")".format(url[0], url[1])

        self._exclude_from_manifest = kwargs.pop("exclude_from_manifest", None)
        if self._exclude_from_manifest is True:
            self._builder += f"\n    .ExcludeFromManifest()"

        self._exclude_from_mcp = kwargs.pop("exclude_from_mcp", None)
        if self._exclude_from_mcp is True:
            self._builder += f"\n    .ExcludeFromMcp()"

        self._explicit_start = kwargs.pop("explicit_start", None)
        if self._explicit_start is True:
            self._builder += f"\n    .WithExplicitStart()"

        self._health_check = kwargs.pop("health_check", None)
        if self._health_check:
            self._builder += f'\n    .WithHealthCheck("{self._health_check}")'

        relationships = kwargs.pop("relationships", None)
        self._relationships: MutableSequence[tuple[Resource, str]] = []
        if relationships:
            if isinstance(relationships, tuple):
                self._relationships = [relationships]
                self._builder += f'\n    .WithRelationship({relationships[0].name}, "{relationships[1]}")'
            else:
                for rel in relationships:
                    self._relationships.append(rel)
                    self._builder += f'\n    .WithRelationship({rel[0].name}, "{rel[1]}")'

        reference_relationships = kwargs.pop("reference_relationships", None)
        self._reference_relationships: MutableSequence[Resource] = []
        if reference_relationships:
            if isinstance(reference_relationships, Resource):
                self._reference_relationships = [reference_relationships]
                self._builder += f'\n    .WithReferenceRelationship({reference_relationships.name})'
            else:
                self._reference_relationships = []
                for reference in reference_relationships:
                    self._builder += f'\n    .WithReferenceRelationship({reference.name})'

        parent_relationships = kwargs.pop("parent_relationships", None)
        self._parent_relationships: MutableSequence[Resource] = []
        if parent_relationships:
            if isinstance(parent_relationships, Resource):
                self._parent_relationships = [parent_relationships]
                self._builder += f'\n    .WithParentRelationship({parent_relationships.name})'
            else:
                self._parent_relationships = []
                for parent in parent_relationships:
                    self._builder += f'\n    .WithParentRelationship({parent.name})'

        child_relationships = kwargs.pop("child_relationships", None)
        self._child_relationships: MutableSequence[Resource] = []
        if child_relationships:
            if isinstance(child_relationships, Resource):
                self._child_relationships = [child_relationships]
                self._builder += f'\n    .WithChildRelationship({child_relationships.name})'
            else:
                self._child_relationships = []
                for child in child_relationships:
                    self._builder += f'\n    .WithChildRelationship({child.name})'

        self._icon_name = kwargs.pop("icon_name", None)
        if self._icon_name:
            if isinstance(self._icon_name, str):
                self._builder += f'\n    .WithIconName("{self._icon_name}")'
            else:
                self._builder += f'\n    .WithIconName("{self._icon_name[0]}", IconVariant.{self._icon_name[1].value})'
        self._builder += ";"


class _ResourceWithArgsOptions(TypedDict, total=False):
    ...


class _ResourceWithEndpointsOptions(TypedDict, total=False):
    ...


class _ResourceWithEnvironmentOptions(TypedDict, total=False):
    ...


class _ResourceWithWaitSupportOptions(TypedDict, total=False):
    ...



class ParameterResourceOptions(_ResourceOptions, total=False):
    description: str | tuple[str, bool]

class ParameterResource(Resource):
    @property
    def package(self) -> str:
        return "#:sdk Aspire.AppHost.Sdk"

    @property
    def description(self) -> str | tuple[str, bool] | None:
        return self._description

    @description.setter
    def description(self, value: str | tuple[str, bool]) -> None:
        if isinstance(value, str):
            self._builder += f"\n{self.name}.WithDescription(\"{value}\");"
        else:
            self._builder += f"\n{self.name}.WithDescription(\"{value[0]}\", {str(value[1]).lower()});"
        self._description = value

    def __init__(self, name: str, builder: str, **kwargs) -> None:
        self._description = kwargs.pop("description", None)
        if self._description:
            if isinstance(self._description, str):
                builder += f"\n    .WithDescription(\"{self._description}\");"
            else:
                builder += f"\n    .WithDescription(\"{self._description[0]}\", {str(self._description[1]).lower()});"
        super().__init__(name, builder=builder, **kwargs)
