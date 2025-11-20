#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from __future__ import annotations
from collections.abc import Mapping
from typing import Any, Iterable, Literal, NoReturn, TypeAlias, TypedDict, MutableSequence, Union, Unpack, cast

from ._models import IconVariant, OtlpProtocol, ProbeType, ProtocolType, ReferenceEnvironment, WaitBehavior

EndpointReference = object  # TODO: implement EndpointReference

class ResourceOptions(TypedDict, total=False):
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
    def url(self) -> NoReturn:
        raise TypeError("url is write-only")

    @url.setter
    def url(self, value: str | tuple[str, str]) -> None:
        if isinstance(value, str):
            self._builder += f"\n{self.name}.WithUrl(\"{value}\");"
        else:
            self._builder += f"\n{self.name}.WithUrl(\"{value[0]}\", \"{value[1]}\");"

    @property
    def exclude_from_manifest(self) -> NoReturn:
        raise TypeError("exclude_from_manifest is write-only")

    @exclude_from_manifest.setter
    def exclude_from_manifest(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.ExcludeFromManifest();"

    @property
    def exclude_from_mcp(self) -> NoReturn:
        raise TypeError("exclude_from_mcp is write-only")

    @exclude_from_mcp.setter
    def exclude_from_mcp(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.ExcludeFromMcp();"

    @property
    def explicit_start(self) -> NoReturn:
        raise TypeError("explicit_start is write-only")

    @explicit_start.setter
    def explicit_start(self, value: Literal[True]) -> None:
        if value is True:
            self._builder += f"\n{self.name}.WithExplicitStart();"

    @property
    def health_check(self) -> NoReturn:
        raise TypeError("health_check is write-only")

    @health_check.setter
    def health_check(self, value: str) -> None:
        self._builder += f'\n{self.name}.WithHealthCheck("{value}");'

    @property
    def relationships(self) -> NoReturn:
        raise TypeError("relationships is write-only")

    @relationships.setter
    def relationships(self, value: tuple[Resource, str] | Iterable[tuple[Resource, str]]) -> None:
        if isinstance(value, tuple) and isinstance(value[0], Resource):
            self._builder += f'\n{self.name}.WithRelationship({value[0].name}, "{value[1]}");'
        else:
            for rel in value:
                rel = cast(tuple[Resource, str], rel)
                self._builder += f'\n{self.name}.WithRelationship({rel[0].name}, "{rel[1]}");'

    @property
    def reference_relationships(self) -> NoReturn:
        raise TypeError("reference_relationships is write-only")

    @reference_relationships.setter
    def reference_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._builder += f'\n{self.name}.WithReferenceRelationship({value.name});'
        else:
            for reference in value:
                self._builder += f'\n{self.name}.WithReferenceRelationship({reference.name});'

    @property
    def parent_relationships(self) -> NoReturn:
        raise TypeError("parent_relationships is write-only")

    @parent_relationships.setter
    def parent_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._builder += f'\n{self.name}.WithParentRelationship({value.name});'
        else:
            for parent in value:
                self._builder += f'\n{self.name}.WithParentRelationship({parent.name});'

    @property
    def child_relationships(self) -> NoReturn:
        raise TypeError("child_relationships is write-only")

    @child_relationships.setter
    def child_relationships(self, value: Resource | Iterable[Resource]) -> None:
        if isinstance(value, Resource):
            self._builder += f'\n{self.name}.WithChildRelationship({value.name});'
        else:
            for child in value:
                self._builder += f'\n{self.name}.WithChildRelationship({child.name});'

    @property
    def icon_name(self) -> NoReturn:
        raise TypeError("icon_name is write-only")

    @icon_name.setter
    def icon_name(self, value: str | tuple[str, IconVariant]) -> None:
        if isinstance(value, str):
            self._builder += f'\n{self.name}.WithIconName("{value}");'
        else:
            self._builder += f'\n{self.name}.WithIconName("{value[0]}", IconVariant.{value[1].value});'

    def __init__(self, name: str, builder: str, **kwargs: Unpack[ResourceOptions]) -> None:
        self.name = name
        self._builder = builder

        if url := kwargs.pop("url", None):
            if isinstance(url, str):
                self._builder += "\n    .WithUrl(\"{}\")".format(url)
            else:
                self._builder += "\n    .WithUrl(\"{}\", \"{}\")".format(url[0], url[1])

        if kwargs.pop("exclude_from_manifest", None) is True:
            self._builder += f"\n    .ExcludeFromManifest()"

        if kwargs.pop("exclude_from_mcp", None) is True:
            self._builder += f"\n    .ExcludeFromMcp()"

        if kwargs.pop("explicit_start", None) is True:
            self._builder += f"\n    .WithExplicitStart()"

        if health_check := kwargs.pop("health_check", None):
            self._builder += f'\n    .WithHealthCheck("{health_check}")'

        if relationships := kwargs.pop("relationships", None):
            if isinstance(relationships, tuple) and isinstance(relationships[0], Resource):
                self._builder += f'\n    .WithRelationship({relationships[0].name}, "{relationships[1]}")'
            else:
                for rel in relationships:
                    rel = cast(tuple[Resource, str], rel)
                    self._builder += f'\n    .WithRelationship({rel[0].name}, "{rel[1]}")'

        if reference_relationships := kwargs.pop("reference_relationships", None):
            if isinstance(reference_relationships, Resource):
                self._builder += f'\n    .WithReferenceRelationship({reference_relationships.name})'
            else:
                for reference in reference_relationships:
                    self._builder += f'\n    .WithReferenceRelationship({reference.name})'

        if parent_relationships := kwargs.pop("parent_relationships", None):
            if isinstance(parent_relationships, Resource):
                self._builder += f'\n    .WithParentRelationship({parent_relationships.name})'
            else:
                for parent in parent_relationships:
                    self._builder += f'\n    .WithParentRelationship({parent.name})'

        if child_relationships := kwargs.pop("child_relationships", None):
            if isinstance(child_relationships, Resource):
                self._builder += f'\n    .WithChildRelationship({child_relationships.name})'
            else:
                for child in child_relationships:
                    self._builder += f'\n    .WithChildRelationship({child.name})'

        if icon_name := kwargs.pop("icon_name", None):
            if isinstance(icon_name, str):
                self._builder += f'\n    .WithIconName("{icon_name}")'
            else:
                self._builder += f'\n    .WithIconName("{icon_name[0]}", IconVariant.{icon_name[1].value})'
        self._builder += ";"


class ResourceWithArgsOptions(TypedDict, total=False):
    args: Iterable[str]


class ResourceWithArgs:
    ...


class EndpointConfiguration(TypedDict, total=False):
    port: int
    target_port: int
    scheme: str
    name: str
    env: str
    is_proxied: bool
    is_external: bool
    protocol: ProtocolType


class HttpHealthCheckConfiguration(TypedDict, total=False):
    path: str
    status_code: int
    endpoint_name: str

class HttpProbeConfiguration(TypedDict, total=False):
    type: ProbeType
    path: str
    initial_delay_seconds: int
    period_seconds: int
    timeout_seconds: int
    failure_threshold: int
    success_threshold: int
    endpoint_name: str

class ResourceWithEndpointsOptions(TypedDict, total=False):
    http2_service: Literal[True]
    endpoint: EndpointConfiguration
    external_http_endpoints: Literal[True]
    http_endpoint: EndpointConfiguration
    https_endpoint: EndpointConfiguration
    http_health_check: HttpHealthCheckConfiguration
    http_probe: HttpProbeConfiguration


class ResourceWithEndpoints:

    def get_endpoint(self, name: str) -> EndpointReference:
        self._builder: str
        self.name: str
        self._builder += f'{self.name}.GetEndpoint("{name}")'
        return EndpointReference()


        # WithHttpEndpoint<T>(this ApplicationModel.IResourceBuilder<T> builder, int? port = null, int? targetPort = null, string? name = null, string? env = null, bool isProxied = true)
        # WithHttpHealthCheck<T>(this ApplicationModel.IResourceBuilder<T> builder, string? path = null, int? statusCode = null, string? endpointName = null)
        # WithHttpProbe<T>(this ApplicationModel.IResourceBuilder<T> builder, ApplicationModel.ProbeType type, string? path = null, int? initialDelaySeconds = null, int? periodSeconds = null, int? timeoutSeconds = null, int? failureThreshold = null, int? successThreshold = null, string? endpointName = null)
        #     where T : ApplicationModel.IResourceWithEndpoints, ApplicationModel.IResourceWithProbes { throw null; }

        # WithHttpsEndpoint<T>(this ApplicationModel.IResourceBuilder<T> builder, int? port = null, int? targetPort = null, string? name = null, string? env = null, bool isProxied = true)
        #     where T : ApplicationModel.IResourceWithEndpoints { throw null; }


class ResourceWithProbesOptions(TypedDict, total=False):
    http_probe: HttpProbeConfiguration


class ResourceWithProbes:
    ...

class ResourceWithServiceDiscoveryOptions(TypedDict, total=False):
    ...

class ResourceWithServiceDiscovery:
    ...

class ResourceWithConnectionStringOptions(TypedDict, total=False):
    publish_as_connection_string: Literal[True]
    connection_string_redirection: ResourceWithConnectionString


class ResourceWithConnectionString:
    def configure_connection_string_manifest_publisher(self) -> None:
        ...

class ExternalServiceResourceOptions(TypedDict, total=False):
    ...


class ExternalServiceResource:
    ...


EnvironmentType: TypeAlias
ReferenceType: TypeAlias = Union[EndpointReference, ExternalServiceResource, ResourceWithServiceDiscovery, tuple[str, str], ResourceWithConnectionString, Mapping[str, Any]]
class ResourceWithEnvironmentOptions(TypedDict, total=False):
    environment: tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None] | Iterable[tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]]
    reference: ReferenceType | Iterable[ReferenceType]
    otlp_exporter: Literal[True] | OtlpProtocol
    reference_environment: ReferenceEnvironment

class ResourceWithEnvironment:
    ...
        #     public static ApplicationModel.IResourceBuilder<T> WithOtlpExporter<T>(this ApplicationModel.IResourceBuilder<T> builder, OtlpProtocol protocol)
        #     where T : ApplicationModel.IResourceWithEnvironment { throw null; }

        # public static ApplicationModel.IResourceBuilder<T> WithOtlpExporter<T>(this ApplicationModel.IResourceBuilder<T> builder)
        #     where T : ApplicationModel.IResourceWithEnvironment { throw null; }
        # WithReference<TDestination>(this ApplicationModel.IResourceBuilder<TDestination> builder, ApplicationModel.EndpointReference endpointReference)
        #     where TDestination : ApplicationModel.IResourceWithEnvironment { throw null; }

        # WithReference<TDestination>(this ApplicationModel.IResourceBuilder<TDestination> builder, ApplicationModel.IResourceBuilder<ApplicationModel.IResourceWithConnectionString> source, string? connectionName = null, bool optional = false)
        #     where TDestination : ApplicationModel.IResourceWithEnvironment { throw null; }

        # WithReference<TDestination>(this ApplicationModel.IResourceBuilder<TDestination> builder, ApplicationModel.IResourceBuilder<ExternalServiceResource> externalService)
        #     where TDestination : ApplicationModel.IResourceWithEnvironment { throw null; }

        # WithReference<TDestination>(this ApplicationModel.IResourceBuilder<TDestination> builder, ApplicationModel.IResourceBuilder<IResourceWithServiceDiscovery> source)
        #     where TDestination : ApplicationModel.IResourceWithEnvironment { throw null; }

        # WithReference<TDestination>(this ApplicationModel.IResourceBuilder<TDestination> builder, string name, System.Uri uri)
        #     where TDestination : ApplicationModel.IResourceWithEnvironment { throw null; }

class ResourceWithWaitSupportOptions(TypedDict, total=False):
    wait_for: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]
    wait_for_completion: Resource | tuple[Resource, int] | Iterable[Resource | tuple[Resource, int]]
    wait_for_start: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]


class ResourceWithWaitSupport:
    ...


class ComputeEnvironmentOptions(TypedDict, total=False):
    ...


class ComputeEnvironmentResource:
    ...


class ComputeResourceOptions(TypedDict, total=False):
    compoute_environment: ComputeEnvironmentResource


class ComputeResource:
    ...


#-------------------------------------------------------------


class ParameterResourceOptions(ResourceOptions, total=False):
    description: str | tuple[str, bool]


class ParameterResource(Resource):
    @property
    def package(self) -> str:
        return "#:sdk Aspire.AppHost.Sdk"

    @property
    def description(self) -> NoReturn:
        raise TypeError("description is write-only")

    @description.setter
    def description(self, value: str | tuple[str, bool]) -> None:
        if isinstance(value, str):
            self._builder += f"\n{self.name}.WithDescription(\"{value}\");"
        else:
            self._builder += f"\n{self.name}.WithDescription(\"{value[0]}\", {str(value[1]).lower()});"

    def __init__(self, name: str, builder: str, **kwargs: Unpack[ParameterResourceOptions]) -> None:
        if description := kwargs.pop("description", None):
            if isinstance(description, str):
                builder += f"\n    .WithDescription(\"{description}\");"
            else:
                builder += f"\n    .WithDescription(\"{description[0]}\", {str(description[1]).lower()});"
        super().__init__(name, builder=builder, **kwargs)



class ProjectResourceOptions(ResourceOptions, total=False):
    disable_forwarded_headers: Literal[True]
    replicas: int


class ProjectResource(Resource):
    ...


class ExecutableResourceOptions(ResourceWithEnvironmentOptions, ResourceWithArgsOptions, ResourceWithEndpointsOptions, ResourceWithWaitSupportOptions, ResourceWithProbesOptions, ComputeResourceOptions, total=False):
    ...

class ExecutableResource(ResourceWithEnvironment, ResourceWithArgs, ResourceWithEndpoints, ResourceWithWaitSupport, ResourceWithProbes, ComputeResource, Resource):
    @property
    def package(self) -> str:
        return "#:sdk Aspire.AppHost.Sdk"

    @property
    def command(self) -> str:
        return self._command

    @command.setter
    def command(self, value: str) -> None:
        self._builder += f'\n{self.name}.WithCommand("{value}");'
        self._command = value

    @property
    def working_directory(self) -> str:
        return self._working_directory

    @working_directory.setter
    def working_directory(self, value: str) -> None:
        self._builder += f'\n{self.name}.WithWorkingDirectory("{value}");'
        self._working_directory = value

    def __init__(self, name: str, command: str, working_directory: str, builder: str, **kwargs: Unpack[ExecutableResourceOptions]) -> None:
        self._command = command
        self._working_directory = working_directory
        super().__init__(name=name, builder=builder, **kwargs)

