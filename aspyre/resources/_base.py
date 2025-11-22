#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from __future__ import annotations
from collections.abc import Mapping
from io import StringIO
from typing import (
    Any,
    Iterable,
    Literal,
    NoReturn,
    Optional,
    Required,
    TypeAlias,
    MutableSequence,
    Union,
    Unpack,
    cast,
)
from typing_extensions import TypedDict

from aspyre._utils import (
    format_bool,
    format_enum,
    format_string,
    format_string_array,
    get_nullable_value,
    get_nullable_from_map,
    get_nullable_from_tuple,
)
from ._models import (
    CertificateTrustScope,
    ContainerLifetime,
    IconVariant,
    OtlpProtocol,
    ProbeType,
    ProtocolType,
    ReferenceEnvironment,
    UnixFileMode,
    WaitBehavior,
    StoreLocation,
    StoreName,
    ImagePullPolicy,
)

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
    relationship: tuple[Resource, str]
    relationships: Iterable[tuple[Resource, str]]
    """Adds a relationship reference to the resource."""
    reference_relationship: Resource
    reference_relationships: Iterable[Resource]
    """Adds a reference relationship reference to the resource."""
    parent_relationship: Resource
    parent_relationships: Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    child_relationship: Resource
    child_relationships: Iterable[Resource]
    """Adds a parent-child relationship reference to the resource."""
    icon_name: str | tuple[str, IconVariant]
    """Specifies the icon to use when displaying the resource in the dashboard. Either icon name string,
    or tuple of (icon_name, icon_variant). The default icon variant is Filled."""
    dockerfile_base_image: Literal[True] | Mapping[str, str]


class Resource:

    @property
    def package(self) -> Iterable[str]:
        return []

    @property
    def url(self) -> NoReturn:
        raise TypeError("url is write-only")

    @url.setter
    def url(self, value: str | tuple[str, str]) -> None:
        if isinstance(value, str):
            self._builder.write(f"\n{self.name}.WithUrl(\"{value}\");")
        else:
            self._builder.write(f"\n{self.name}.WithUrl(\"{value[0]}\", \"{value[1]}\");")

    @property
    def exclude_from_manifest(self) -> NoReturn:
        raise TypeError("exclude_from_manifest is write-only")

    @exclude_from_manifest.setter
    def exclude_from_manifest(self, value: Literal[True]) -> None:
        if value is True:
            self._builder.write(f"\n{self.name}.ExcludeFromManifest();")

    @property
    def exclude_from_mcp(self) -> NoReturn:
        raise TypeError("exclude_from_mcp is write-only")

    @exclude_from_mcp.setter
    def exclude_from_mcp(self, value: Literal[True]) -> None:
        if value is True:
            self._builder.write(f"\n{self.name}.ExcludeFromMcp();")

    @property
    def explicit_start(self) -> NoReturn:
        raise TypeError("explicit_start is write-only")

    @explicit_start.setter
    def explicit_start(self, value: Literal[True]) -> None:
        if value is True:
            self._builder.write(f"\n{self.name}.WithExplicitStart();")

    @property
    def health_check(self) -> NoReturn:
        raise TypeError("health_check is write-only")

    @health_check.setter
    def health_check(self, value: str) -> None:
        self._builder.write(f'\n{self.name}.WithHealthCheck("{value}");')

    @property
    def relationship(self) -> NoReturn:
        raise TypeError("relationship is write-only")

    @relationship.setter
    def relationship(self, value: tuple[Resource, str]) -> None:
        self._builder.write(f'\n{self.name}.WithRelationship({value[0].name}.Resource, "{value[1]}");')

    @property
    def relationships(self) -> NoReturn:
        raise TypeError("relationships is write-only")

    @relationships.setter
    def relationships(self, value: Iterable[tuple[Resource, str]]) -> None:
        for rel in value:
            self._builder.write(f'\n{self.name}.WithRelationship({rel[0].name}.Resource, "{rel[1]}");')

    @property
    def reference_relationship(self) -> NoReturn:
        raise TypeError("reference_relationship is write-only")

    @reference_relationship.setter
    def reference_relationship(self, value: Resource) -> None:
        self._builder.write(f'\n{self.name}.WithReferenceRelationship({value.name});')

    @property
    def reference_relationships(self) -> NoReturn:
        raise TypeError("reference_relationships is write-only")

    @reference_relationships.setter
    def reference_relationships(self, value: Iterable[Resource]) -> None:
        for reference in value:
            self._builder.write(f'\n{self.name}.WithReferenceRelationship({reference.name});')

    @property
    def parent_relationship(self) -> NoReturn:
        raise TypeError("parent_relationship is write-only")

    @parent_relationship.setter
    def parent_relationship(self, value: Resource) -> None:
        self._builder.write(f'\n{self.name}.WithParentRelationship({value.name});')

    @property
    def parent_relationships(self) -> NoReturn:
        raise TypeError("parent_relationships is write-only")

    @parent_relationships.setter
    def parent_relationships(self, value: Iterable[Resource]) -> None:
        for parent in value:
            self._builder.write(f'\n{self.name}.WithParentRelationship({parent.name});')

    @property
    def child_relationship(self) -> NoReturn:
        raise TypeError("child_relationship is write-only")

    @child_relationship.setter
    def child_relationship(self, value: Resource) -> None:
        self._builder.write(f'\n{self.name}.WithChildRelationship({value.name});')

    @property
    def child_relationships(self) -> NoReturn:
        raise TypeError("child_relationships is write-only")

    @child_relationships.setter
    def child_relationships(self, value: Iterable[Resource]) -> None:
        for child in value:
            self._builder.write(f'\n{self.name}.WithChildRelationship({child.name});')

    @property
    def icon_name(self) -> NoReturn:
        raise TypeError("icon_name is write-only")

    @icon_name.setter
    def icon_name(self, value: str | tuple[str, IconVariant]) -> None:
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithIconName("{value}");')
        else:
            self._builder.write(f'\n{self.name}.WithIconName("{value[0]}", IconVariant.{value[1].value});')

    @property
    def dockerfile_base_image(self) -> NoReturn:
        raise TypeError("dockerfile_base_image is write-only")

    @dockerfile_base_image.setter
    def dockerfile_base_image(self, value: Literal[True] | Mapping[str, str]) -> None:
        if value is True:
            self._builder.write(f'\n{self.name}.WithDockerfileBaseImage();')
        else:
            build_image = get_nullable_from_map(value, "build_image")
            runtime_image = get_nullable_from_map(value, "runtime_image")
            self._builder.write(f'\n{self.name}.WithDockerfileBaseImage({build_image}, {runtime_image});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceOptions]) -> None:
        self.name = name
        self._builder = builder
        if url := kwargs.pop("url", None):
            if isinstance(url, str):
                self._builder.write(f"\n    .WithUrl({format_string(url)})")
            else:
                self._builder.write(f"\n    .WithUrl({format_string(url[0])}, {format_string(url[1])})")
        if kwargs.pop("exclude_from_manifest", None) is True:
            self._builder.write(f"\n    .ExcludeFromManifest()")
        if kwargs.pop("exclude_from_mcp", None) is True:
            self._builder.write(f"\n    .ExcludeFromMcp()")
        if kwargs.pop("explicit_start", None) is True:
            self._builder.write(f"\n    .WithExplicitStart()")
        if health_check := kwargs.pop("health_check", None):
            self._builder.write(f'\n    .WithHealthCheck({format_string(health_check)})')
        if relationship := kwargs.pop("relationship", None):
            self._builder.write(f'\n    .WithRelationship({relationship[0].name}.Resource, {format_string(relationship[1])})')
        if relationships := kwargs.pop("relationships", None):
            for rel in relationships:
                self._builder.write(f'\n    .WithRelationship({rel[0].name}.Resource, {format_string(rel[1])})')
        if reference_relationship := kwargs.pop("reference_relationship", None):
            self._builder.write(f'\n    .WithReferenceRelationship({reference_relationship.name})')
        if reference_relationships := kwargs.pop("reference_relationships", None):
            for reference in reference_relationships:
                self._builder.write(f'\n    .WithReferenceRelationship({reference.name})')
        if parent_relationship := kwargs.pop("parent_relationship", None):
            self._builder.write(f'\n    .WithParentRelationship({parent_relationship.name})')
        if parent_relationships := kwargs.pop("parent_relationships", None):
            for parent in parent_relationships:
                self._builder.write(f'\n    .WithParentRelationship({parent.name})')
        if child_relationship := kwargs.pop("child_relationship", None):
            self._builder.write(f'\n    .WithChildRelationship({child_relationship.name})')
        if child_relationships := kwargs.pop("child_relationships", None):
            for child in child_relationships:
                self._builder.write(f'\n    .WithChildRelationship({child.name})')
        if icon_name := kwargs.pop("icon_name", None):
            if isinstance(icon_name, str):
                self._builder.write(f'\n    .WithIconName({format_string(icon_name)})')
            else:
                self._builder.write(f'\n    .WithIconName({format_string(icon_name[0])}, {format_enum(icon_name[1])})')
        if dockerfile_base_image := kwargs.pop("dockerfile_base_image", None):
            if dockerfile_base_image is True:
                self._builder.write(f'\n    .WithDockerfileBaseImage()')
            else:
                build_image = get_nullable_from_map(dockerfile_base_image, "build_image")
                runtime_image = get_nullable_from_map(dockerfile_base_image, "runtime_image")
                self._builder.write(f'\n    .WithDockerfileBaseImage({build_image}, {runtime_image})')
        self._builder.write(";")


class ResourceWithArgsOptions(TypedDict, total=False):
    args: Iterable[str]
    certificate_trust_scope: CertificateTrustScope
    developer_certificate_trust: bool
    certificate_authority_collection: CertificateAuthorityCollection


class ResourceWithArgs:
    @property
    def args(self) -> NoReturn:
        raise TypeError("args is write-only")

    @args.setter
    def args(self, value: Iterable[str]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithArgs({format_string_array(value)});')

    @property
    def certificate_trust_scope(self) -> NoReturn:
        raise TypeError("certificate_trust_scope is write-only")

    @certificate_trust_scope.setter
    def certificate_trust_scope(self, value: CertificateTrustScope) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateTrustScope({format_enum(value)});')

    @property
    def developer_certificate_trust(self) -> NoReturn:
        raise TypeError("developer_certificate_trust is write-only")

    @developer_certificate_trust.setter
    def developer_certificate_trust(self, value: bool) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust({format_bool(value)});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithArgsOptions]) -> None:
        if args := kwargs.get("args", None):
            builder.write(f'\n    .WithArgs({format_string_array(args)})')
        if certificate_trust_scope := kwargs.get("certificate_trust_scope", None):
            builder.write(f'\n    .WithCertificateTrustScope({format_enum(certificate_trust_scope)})')
        if developer_certificate_trust := kwargs.get("developer_certificate_trust", None):
            builder.write(f'\n    .WithDeveloperCertificateTrust({format_bool(developer_certificate_trust)})')
        super().__init__(name=name, builder=builder, **kwargs) # type: ignore Assume Resource is a base class


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
    type: Required[ProbeType]
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
    @property
    def http2_service(self) -> NoReturn:
        raise TypeError("http2_service is write-only")

    @http2_service.setter
    def http2_service(self, value: Literal[True]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AsHttp2Service();')

    @property
    def endpoint(self) -> NoReturn:
        raise TypeError("endpoint is write-only")

    @endpoint.setter
    def endpoint(self, value: EndpointConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(value, "port")
        target_port = get_nullable_from_map(value, "target_port")
        scheme = get_nullable_from_map(value, "scheme")
        name = get_nullable_from_map(value, "name")
        env = get_nullable_from_map(value, "env")
        is_proxied = get_nullable_from_map(value, "is_proxied", True)
        is_external = get_nullable_from_map(value, "is_external", False)
        protocol = get_nullable_from_map(value, "protocol")
        self._builder.write(f'\n{self.name}.WithEndpoint({port}, {target_port}, {scheme}, {name}, {env}, {is_proxied}, {is_external}, {protocol});')

    @property
    def external_http_endpoints(self) -> NoReturn:
        raise TypeError("external_http_endpoints is write-only")

    @external_http_endpoints.setter
    def external_http_endpoints(self, value: Literal[True]) -> None:
        self._builder: StringIO
        self.name: str
        if value is True:
            self._builder.write(f'\n{self.name}.WithExternalHttpEndpoints();')

    @property
    def http_endpoint(self) -> NoReturn:
        raise TypeError("http_endpoint is write-only")

    @http_endpoint.setter
    def http_endpoint(self, value: EndpointConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(value, "port")
        target_port = get_nullable_from_map(value, "target_port")
        name = get_nullable_from_map(value, "name")
        env = get_nullable_from_map(value, "env")
        is_proxied = get_nullable_from_map(value, "is_proxied", True)
        self._builder.write(f'\n{self.name}.WithHttpEndpoint({port}, {target_port}, {name}, {env}, {is_proxied});')

    @property
    def https_endpoint(self) -> NoReturn:
        raise TypeError("https_endpoint is write-only")

    @https_endpoint.setter
    def https_endpoint(self, value: EndpointConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(value, "port")
        target_port = get_nullable_from_map(value, "target_port")
        name = get_nullable_from_map(value, "name")
        env = get_nullable_from_map(value, "env")
        is_proxied = get_nullable_from_map(value, "is_proxied", True)
        self._builder.write(f'\n{self.name}.WithHttpsEndpoint({port}, {target_port}, {name}, {env}, {is_proxied});')

    @property
    def http_health_check(self) -> NoReturn:
        raise TypeError("http_health_check is write-only")

    @http_health_check.setter
    def http_health_check(self, value: HttpHealthCheckConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        path = get_nullable_from_map(value, "path")
        status_code = get_nullable_from_map(value, "status_code")
        endpoint_name = get_nullable_from_map(value, "endpoint_name")
        self._builder.write(f'\n{self.name}.WithHttpHealthCheck({path}, {status_code}, {endpoint_name});')

    @property
    def http_probe(self) -> NoReturn:
        raise TypeError("http_probe is write-only")

    @http_probe.setter
    def http_probe(self, value: HttpProbeConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        path = get_nullable_from_map(value, "path")
        initial_delay_seconds = get_nullable_from_map(value, "initial_delay_seconds")
        period_seconds = get_nullable_from_map(value, "period_seconds")
        timeout_seconds = get_nullable_from_map(value, "timeout_seconds")
        failure_threshold = get_nullable_from_map(value, "failure_threshold")
        success_threshold = get_nullable_from_map(value, "success_threshold")
        endpoint_name = get_nullable_from_map(value, "endpoint_name")
        self._builder.write(f'\n{self.name}.WithHttpProbe({format_enum(value["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithEndpointsOptions]) -> None:
        if kwargs.get("http2_service", None) is True:
            builder.write(f'\n    .AsHttp2Service()')
        if endpoint := kwargs.get("endpoint", None):
            port = get_nullable_from_map(endpoint, "port")
            target_port = get_nullable_from_map(endpoint, "target_port")
            scheme = get_nullable_from_map(endpoint, "scheme")
            name_ = get_nullable_from_map(endpoint, "name")
            env = get_nullable_from_map(endpoint, "env")
            is_proxied = get_nullable_from_map(endpoint, "is_proxied", True)
            is_external = get_nullable_from_map(endpoint, "is_external", False)
            protocol = get_nullable_from_map(endpoint, "protocol")
            builder.write(f'\n    .WithEndpoint({port}, {target_port}, {scheme}, {name_}, {env}, {is_proxied}, {is_external}, {protocol})')
        if kwargs.get("external_http_endpoints", None) is True:
            builder.write(f'\n    .WithExternalHttpEndpoints()')
        if http_endpoint := kwargs.get("http_endpoint", None):
            port = get_nullable_from_map(http_endpoint, "port")
            target_port = get_nullable_from_map(http_endpoint, "target_port")
            name_ = get_nullable_from_map(http_endpoint, "name")
            env = get_nullable_from_map(http_endpoint, "env")
            is_proxied = get_nullable_from_map(http_endpoint, "is_proxied", True)
            builder.write(f'\n    .WithHttpEndpoint({port}, {target_port}, {name_}, {env}, {is_proxied})')
        if https_endpoint := kwargs.get("https_endpoint", None):
            port = get_nullable_from_map(https_endpoint, "port")
            target_port = get_nullable_from_map(https_endpoint, "target_port")
            name_ = get_nullable_from_map(https_endpoint, "name")
            env = get_nullable_from_map(https_endpoint, "env")
            is_proxied = get_nullable_from_map(https_endpoint, "is_proxied", True)
            builder.write(f'\n    .WithHttpsEndpoint({port}, {target_port}, {name_}, {env}, {is_proxied})')
        if http_health_check := kwargs.get("http_health_check", None):
            path = get_nullable_from_map(http_health_check, "path")
            status_code = get_nullable_from_map(http_health_check, "status_code")
            endpoint_name = get_nullable_from_map(http_health_check, "endpoint_name")
            builder.write(f'\n    .WithHttpHealthCheck({path}, {status_code}, {endpoint_name})')
        if http_probe := kwargs.get("http_probe", None):
            path = get_nullable_from_map(http_probe, "path")
            initial_delay_seconds = get_nullable_from_map(http_probe, "initial_delay_seconds")
            period_seconds = get_nullable_from_map(http_probe, "period_seconds")
            timeout_seconds = get_nullable_from_map(http_probe, "timeout_seconds")
            failure_threshold = get_nullable_from_map(http_probe, "failure_threshold")
            success_threshold = get_nullable_from_map(http_probe, "success_threshold")
            endpoint_name = get_nullable_from_map(http_probe, "endpoint_name")
            builder.write(f'\n    .WithHttpProbe({format_enum(http_probe["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name})')
        super().__init__(name=name, builder=builder, **kwargs) # type: ignore Assuming multiple inheritance with Resource


class ResourceWithProbesOptions(TypedDict, total=False):
    http_probe: HttpProbeConfiguration


class ResourceWithProbes:
    @property
    def http_probe(self) -> NoReturn:
        raise TypeError("http_probe is write-only")

    @http_probe.setter
    def http_probe(self, value: HttpProbeConfiguration) -> None:
        self._builder: StringIO
        self.name: str
        path = get_nullable_from_map(value, "path")
        initial_delay_seconds = get_nullable_from_map(value, "initial_delay_seconds")
        period_seconds = get_nullable_from_map(value, "period_seconds")
        timeout_seconds = get_nullable_from_map(value, "timeout_seconds")
        failure_threshold = get_nullable_from_map(value, "failure_threshold")
        success_threshold = get_nullable_from_map(value, "success_threshold")
        endpoint_name = get_nullable_from_map(value, "endpoint_name")
        self._builder.write(f'\n{self.name}.WithHttpProbe({format_enum(value["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithProbesOptions]) -> None:
        if http_probe := kwargs.pop("http_probe", None):
            path = get_nullable_from_map(http_probe, "path")
            initial_delay_seconds = get_nullable_from_map(http_probe, "initial_delay_seconds")
            period_seconds = get_nullable_from_map(http_probe, "period_seconds")
            timeout_seconds = get_nullable_from_map(http_probe, "timeout_seconds")
            failure_threshold = get_nullable_from_map(http_probe, "failure_threshold")
            success_threshold = get_nullable_from_map(http_probe, "success_threshold")
            endpoint_name = get_nullable_from_map(http_probe, "endpoint_name")
            builder.write(f'\n    .WithHttpProbe({format_enum(http_probe["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name})')
        super().__init__(name=name, builder=builder, **kwargs) # type: ignore Assuming multiple inheritance with Resource


class ResourceWithServiceDiscoveryOptions(ResourceWithEndpointsOptions, total=False):
    ...


class ResourceWithServiceDiscovery(ResourceWithEndpoints):
    ...


class ResourceWithConnectionStringOptions(TypedDict, total=False):
    connection_string_redirection: ResourceWithConnectionString


class ResourceWithConnectionString:
    @property
    def connection_string_redirection(self) -> NoReturn:
        raise TypeError("connection_string_redirection is write-only")

    @connection_string_redirection.setter
    def connection_string_redirection(self, value: ResourceWithConnectionString) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithConnectionStringRedirection({value.name}.Resource);')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithConnectionStringOptions]) -> None:
        if connection_string_redirection := kwargs.get("connection_string_redirection", None):
            builder.write(f'\n    .WithConnectionStringRedirection({connection_string_redirection.name}.Resource)')
        super().__init__(name=name, builder=builder, **kwargs) # type: ignore Assuming multiple inheritance with Resource


class ResourceWithEnvironmentOptions(TypedDict, total=False):
    environment: tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]
    environments: Iterable[tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]]
    reference: EndpointReference | ExternalServiceResource | ResourceWithServiceDiscovery | tuple[str, str] | ResourceWithConnectionString
    references: Iterable[EndpointReference | ExternalServiceResource | ResourceWithServiceDiscovery | tuple[str, str] | ResourceWithConnectionString]
    otlp_exporter: Literal[True] | OtlpProtocol
    reference_environment: ReferenceEnvironment
    certificate_trust_scope: CertificateTrustScope
    developer_certificate_trust: bool
    certificate_authority_collection: CertificateAuthorityCollection


class ResourceWithEnvironment:
    @property
    def environment(self) -> NoReturn:
        raise TypeError("environment is write-only")

    @environment.setter
    def environment(self, value: tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]) -> None:
        name, ref = value
        self._builder: StringIO
        self.name: str
        # if isinstance(ref, EndpointReference):
        #     self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {ref});')  # TODO: fix EndpointReference string representation
        if isinstance(ref, ParameterResource) or isinstance(ref, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {cast(Resource, ref).name});')
        elif isinstance(ref, ExternalServiceResource):
            self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {cast(Resource, ref).name});')
        else:
            self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {get_nullable_value(ref)});')
    @property
    def environments(self) -> NoReturn:
        raise TypeError("environments is write-only")

    @environments.setter
    def environments(self, value: Iterable[tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]]) -> None:
        self._builder: StringIO
        self.name: str
        for env in value:
            name, ref = env
            # if isinstance(ref, EndpointReference):
            #     self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {ref});')  # TODO: fix EndpointReference string representation
            if isinstance(ref, ParameterResource) or isinstance(ref, ResourceWithConnectionString):
                self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {ref.name});')
            elif isinstance(ref, ExternalServiceResource):
                self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {ref.name});')
            else:
                self._builder.write(f'\n{self.name}.WithEnvironment({format_string(name)}, {get_nullable_value(ref)});')

    @property
    def reference(self) -> NoReturn:
        raise TypeError("reference is write-only")

    @reference.setter
    def reference(self, value: EndpointReference | ExternalServiceResource | ResourceWithServiceDiscovery | tuple[str, str] | ResourceWithConnectionString | Mapping[str, Any]) -> None:
        self._builder: StringIO
        self.name: str
        # if isinstance(value, EndpointReference):
        #     self._builder.write(f'\n{self.name}.WithReference({value});')  # TODO: fix EndpointReference string representation
        if isinstance(value, ExternalServiceResource):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')
        elif isinstance(value, ResourceWithServiceDiscovery):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')
        elif isinstance(value, tuple):
            self._builder.write(f'\n{self.name}.WithReference({format_string(value[0])}, {format_string(value[1])});')
        elif isinstance(value, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')

    @property
    def references(self) -> NoReturn:
        raise TypeError("references is write-only")

    @references.setter
    def references(self, value: Iterable[EndpointReference | ExternalServiceResource | ResourceWithServiceDiscovery | tuple[str, str] | ResourceWithConnectionString]) -> None:
        self._builder: StringIO
        self.name: str
        for ref in value:
            # if isinstance(ref, EndpointReference):
            #     self._builder.write(f'\n{self.name}.WithReference({ref});')  # TODO: fix EndpointReference string representation
            if isinstance(ref, ExternalServiceResource):
                self._builder.write(f'\n{self.name}.WithReference({cast(Resource, ref).name});')
            elif isinstance(ref, ResourceWithServiceDiscovery):
                self._builder.write(f'\n{self.name}.WithReference({cast(Resource, ref).name});')
            elif isinstance(ref, tuple):
                self._builder.write(f'\n{self.name}.WithReference({format_string(ref[0])}, {format_string(ref[1])});')
            elif isinstance(ref, ResourceWithConnectionString):  # TODO: Missing IResourceWithConnectionString> source, string? connectionName = null, bool optional = false
                self._builder.write(f'\n{self.name}.WithReference({cast(Resource, ref).name});')

    @property
    def otlp_exporter(self) -> NoReturn:
        raise TypeError("otlp_exporter is write-only")

    @otlp_exporter.setter
    def otlp_exporter(self, value: Literal[True] | OtlpProtocol) -> None:
        self._builder: StringIO
        self.name: str
        if value is True:
            self._builder.write(f'\n{self.name}.WithOtlpExporter();')
        else:
            self._builder.write(f'\n{self.name}.WithOtlpExporter({format_enum(value)});')

    @property
    def reference_environment(self) -> NoReturn:
        raise TypeError("reference_environment is write-only")

    @reference_environment.setter
    def reference_environment(self, value: ReferenceEnvironment) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithReferenceEnvironment({format_enum(value)});')

    @property
    def certificate_trust_scope(self) -> NoReturn:
        raise TypeError("certificate_trust_scope is write-only")

    @certificate_trust_scope.setter
    def certificate_trust_scope(self, value: CertificateTrustScope) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateTrustScope({format_enum(value)});')

    @property
    def developer_certificate_trust(self) -> NoReturn:
        raise TypeError("developer_certificate_trust is write-only")

    @developer_certificate_trust.setter
    def developer_certificate_trust(self, value: bool) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust({format_bool(value)});')

    @property
    def certificate_authority_collection(self) -> NoReturn:
        raise TypeError("certificate_authority_collection is write-only")

    @certificate_authority_collection.setter
    def certificate_authority_collection(self, value: CertificateAuthorityCollection) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateAuthorityCollection({cast(Resource, value).name});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithEnvironmentOptions]) -> None:
        if environment := kwargs.pop("environment", None):
            env_name, ref = environment
            # if isinstance(ref, EndpointReference):
            #     builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {ref})')
            if isinstance(ref, ParameterResource) or isinstance(ref, ResourceWithConnectionString):
                builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {cast(Resource, ref).name})')
            elif isinstance(ref, ExternalServiceResource):
                builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {cast(Resource, ref).name})')
            else:
                builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {get_nullable_value(ref)})')
        if environments := kwargs.pop("environments", None):
            for env in environments:
                env_name, ref = env
                # if isinstance(ref, EndpointReference):
                #     builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {ref})')
                if isinstance(ref, ParameterResource) or isinstance(ref, ResourceWithConnectionString):
                    builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {cast(Resource, ref).name})')
                elif isinstance(ref, ExternalServiceResource):
                    builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {cast(Resource, ref).name})')
                else:
                    builder.write(f'\n    .WithEnvironment({format_string(env_name)}, {get_nullable_value(ref)})')
        if reference := kwargs.pop("reference", None):
            # if isinstance(reference, EndpointReference):
            #     builder.write(f'\n    .WithReference({reference})')
            if isinstance(reference, ExternalServiceResource):
                builder.write(f'\n    .WithReference({cast(Resource, reference).name})')
            elif isinstance(reference, ResourceWithServiceDiscovery):
                builder.write(f'\n    .WithReference({cast(Resource, reference).name})')
            elif isinstance(reference, tuple):
                builder.write(f'\n    .WithReference({format_string(reference[0])}, {format_string(reference[1])})')
            elif isinstance(reference, ResourceWithConnectionString):
                builder.write(f'\n    .WithReference({cast(Resource, reference).name})')
        if references := kwargs.pop("references", None):
            for ref in references:
                if isinstance(ref, ExternalServiceResource):
                    builder.write(f'\n    .WithReference({cast(Resource, ref).name})')
                elif isinstance(ref, ResourceWithServiceDiscovery):
                    builder.write(f'\n    .WithReference({cast(Resource, ref).name})')
                elif isinstance(ref, tuple):
                    builder.write(f'\n    .WithReference({format_string(ref[0])}, {format_string(ref[1])})')
                elif isinstance(ref, ResourceWithConnectionString):
                    builder.write(f'\n    .WithReference({cast(Resource, ref).name})')
                # elif isinstance(ref, EndpointReference):
                #     builder.write(f'\n    .WithReference({ref})')
        if otlp_exporter := kwargs.pop("otlp_exporter", None):
            if otlp_exporter is True:
                builder.write(f'\n    .WithOtlpExporter()')
            else:
                builder.write(f'\n    .WithOtlpExporter({format_enum(otlp_exporter)})')
        if reference_environment := kwargs.pop("reference_environment", None):
            builder.write(f'\n    .WithReferenceEnvironment({format_enum(reference_environment)})')
        if certificate_trust_scope := kwargs.pop("certificate_trust_scope", None):
            builder.write(f'\n    .WithCertificateTrustScope({format_enum(certificate_trust_scope)})')
        if developer_certificate_trust := kwargs.pop("developer_certificate_trust", None):
            builder.write(f'\n    .WithDeveloperCertificateTrust({format_bool(developer_certificate_trust)})')
        if certificate_authority_collection := kwargs.pop("certificate_authority_collection", None):
            builder.write(f'\n    .WithCertificateAuthorityCollection({cast(Resource, certificate_authority_collection).name})')
        super().__init__(name=name, builder=builder, **kwargs) # type: ignore Assuming multiple inheritance with Resource


class ResourceWithWaitSupportOptions(TypedDict, total=False):
    wait_for: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]
    wait_for_completion: Resource | tuple[Resource, int] | Iterable[Resource | tuple[Resource, int]]
    wait_for_start: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]


class ResourceWithWaitSupport:
    @property
    def wait_for(self) -> NoReturn:
        raise TypeError("wait_for is write-only")

    @wait_for.setter
    def wait_for(self, value: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitFor({value.name});')
        elif isinstance(value, tuple) and isinstance(value[0], Resource):
            self._builder.write(f'\n{self.name}.WaitFor({value[0].name}, {format_enum(cast(WaitBehavior, value[1]))});')
        else:
            for item in value:
                if isinstance(item, Resource):
                    self._builder.write(f'\n{self.name}.WaitFor({item.name});')
                else:
                    item = cast(tuple[Resource, WaitBehavior], item)
                    self._builder.write(f'\n{self.name}.WaitFor({item[0].name}, {format_enum(item[1])});')

    @property
    def wait_for_completion(self) -> NoReturn:
        raise TypeError("wait_for_completion is write-only")

    @wait_for_completion.setter
    def wait_for_completion(self, value: Resource | tuple[Resource, int] | Iterable[Resource | tuple[Resource, int]]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitForCompletion({value.name});')
        elif isinstance(value, tuple) and isinstance(value[0], Resource):
            self._builder.write(f'\n{self.name}.WaitForCompletion({value[0].name}, {value[1]});')
        else:
            for item in value:
                if isinstance(item, Resource):
                    self._builder.write(f'\n{self.name}.WaitForCompletion({item.name});')
                else:
                    item = cast(tuple[Resource, int], item)
                    self._builder.write(f'\n{self.name}.WaitForCompletion({item[0].name}, {item[1]});')

    @property
    def wait_for_start(self) -> NoReturn:
        raise TypeError("wait_for_start is write-only")

    @wait_for_start.setter
    def wait_for_start(self, value: Resource | tuple[Resource, WaitBehavior] | Iterable[Resource | tuple[Resource, WaitBehavior]]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitForStart({value.name});')
        elif isinstance(value, tuple) and isinstance(value[0], Resource):
            self._builder.write(f'\n{self.name}.WaitForStart({value[0].name}, {format_enum(cast(WaitBehavior, value[1]))});')
        else:
            for item in value:
                if isinstance(item, Resource):
                    self._builder.write(f'\n{self.name}.WaitForStart({item.name});')
                else:
                    item = cast(tuple[Resource, WaitBehavior], item)
                    self._builder.write(f'\n{self.name}.WaitForStart({item[0].name}, {format_enum(item[1])});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithWaitSupportOptions]) -> None:
        if wait_for := kwargs.pop("wait_for", None):
            if isinstance(wait_for, Resource):
                builder.write(f'\n    .WaitFor({wait_for.name})')
            elif isinstance(wait_for, tuple) and isinstance(wait_for[0], Resource):
                builder.write(f'\n    .WaitFor({wait_for[0].name}, {format_enum(cast(WaitBehavior, wait_for[1]))})')
            else:
                for item in wait_for:
                    if isinstance(item, Resource):
                        builder.write(f'\n    .WaitFor({item.name})')
                    else:
                        item = cast(tuple[Resource, WaitBehavior], item)
                        builder.write(f'\n    .WaitFor({item[0].name}, {format_enum(item[1])})')
        if wait_for_completion := kwargs.pop("wait_for_completion", None):
            if isinstance(wait_for_completion, Resource):
                builder.write(f'\n    .WaitForCompletion({wait_for_completion.name})')
            elif isinstance(wait_for_completion, tuple) and isinstance(wait_for_completion[0], Resource):
                builder.write(f'\n    .WaitForCompletion({wait_for_completion[0].name}, {wait_for_completion[1]})')
            else:
                for item in wait_for_completion:
                    if isinstance(item, Resource):
                        builder.write(f'\n    .WaitForCompletion({item.name})')
                    else:
                        item = cast(tuple[Resource, int], item)
                        builder.write(f'\n    .WaitForCompletion({item[0].name}, {item[1]})')
        if wait_for_start := kwargs.pop("wait_for_start", None):
            if isinstance(wait_for_start, Resource):
                builder.write(f'\n    .WaitForStart({wait_for_start.name})')
            elif isinstance(wait_for_start, tuple) and isinstance(wait_for_start[0], Resource):
                builder.write(f'\n    .WaitForStart({wait_for_start[0].name}, {format_enum(cast(WaitBehavior, wait_for_start[1]))})')
            else:
                for item in wait_for_start:
                    if isinstance(item, Resource):
                        builder.write(f'\n    .WaitForStart({item.name})')
                    else:
                        item = cast(tuple[Resource, WaitBehavior], item)
                        builder.write(f'\n    .WaitForStart({item[0].name}, {format_enum(item[1])})')

        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance


class ComputeEnvironmentOptions(TypedDict, total=False):
    ...


class ComputeEnvironmentResource:
    ...


class ComputeResourceOptions(TypedDict, total=False):
    compoute_environment: ComputeEnvironmentResource


class ComputeResource:
    @property
    def compute_environment(self) -> NoReturn:
        raise TypeError("compute_environment is write-only")

    @compute_environment.setter
    def compute_environment(self, value: ComputeEnvironmentResource) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithComputeEnvironment({cast(Resource, value).name});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ComputeResourceOptions]) -> None:
        if compute_environment := kwargs.pop("compute_environment", None):
            builder.write(f'\n    .WithComputeEnvironment({cast(Resource, compute_environment).name})')
        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance


class ResourceWithContainerFilesOptions(TypedDict, total=False):
    container_files_source: str
    clear_container_files_sources: Literal[True]


class ResourceWithContainerFiles:
    @property
    def container_files_source(self) -> NoReturn:
        raise TypeError("container_files_source is write-only")

    @container_files_source.setter
    def container_files_source(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AddContainerFilesSource({format_string(value)});')

    @property
    def clear_container_files_sources(self) -> NoReturn:
        raise TypeError("clear_container_files_sources is write-only")

    @clear_container_files_sources.setter
    def clear_container_files_sources(self, value: Literal[True]) -> None:
        if value is True:
            self._builder: StringIO
            self.name: str
            self._builder.write(f'\n{self.name}.ClearContainerFilesSources();')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithContainerFilesOptions]) -> None:
        if container_files_source := kwargs.pop("container_files_source", None):
            builder.write(f'\n    .AddContainerFilesSource({format_string(container_files_source)})')
        if kwargs.pop("clear_container_files_sources", None) is True:
            builder.write(f'\n    .ClearContainerFilesSources()')
        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance


class ContainerFilesDestinationResourceOptions(TypedDict, total=False):
    publish_with_container_files: tuple[ResourceWithContainerFiles, str]


class ContainerFilesDestinationResource:
    @property
    def publish_with_container_files(self) -> NoReturn:
        raise TypeError("publish_with_container_files is write-only")

    @publish_with_container_files.setter
    def publish_with_container_files(self, value: tuple[ResourceWithContainerFiles, str]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.PublishWithContainerFiles({cast(Resource, value[0]).name}, {format_string(value[1])});')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ContainerFilesDestinationResourceOptions]) -> None:
        if publish_with_container_files := kwargs.pop("publish_with_container_files", None):
            builder.write(f'\n    .PublishWithContainerFiles({cast(Resource, publish_with_container_files[0]).name}, {format_string(publish_with_container_files[1])})')
        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance

#-------------------------------------------------------------


class ExternalServiceResource(Resource):
    ...

class CertificateAuthorityCollectionOptions(ResourceOptions, total=False):
    certificate: bytes | str
    certificates: Iterable[bytes | str]
    certificates_from_store: tuple[StoreName, StoreLocation]  # TODO: support filter
    certificates_from_file: str  # TODO: support filter


class CertificateAuthorityCollection(Resource):

    @property
    def package(self) -> Iterable[str]:
        return ["using System.Security.Cryptography.X509Certificates;"]

    @property
    def certificate(self) -> NoReturn:
        raise TypeError("certificate is write-only")

    @certificate.setter
    def certificate(self, value: bytes | str) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, bytes):
            # TODO: This will need X509Certificate2 certificate = X509CertificateLoader.LoadCertificate(certData);
            self._builder.write(f'\n{self.name}.AddCertificate(Convert.FromBase64String("{value.decode()}"));')
        else:
            self._builder.write(f'\n{self.name}.AddCertificate(File.ReadAllText("{value}"));')

    @property
    def certificates(self) -> NoReturn:
        raise TypeError("certificates is write-only")

    @certificates.setter
    def certificates(self, value: Iterable[bytes | str]) -> None:
        self._builder: StringIO
        self.name: str
        for cert in value:
            if isinstance(cert, bytes):
                self._builder.write(f'\n{self.name}.AddCertificate(Convert.FromBase64String("{cert.decode()}"))')
            else:
                self._builder.write(f'\n{self.name}.AddCertificate(File.ReadAllText("{cert}"))')
    @property
    def certificates_from_store(self) -> NoReturn:
        raise TypeError("certificates_from_store is write-only")

    @certificates_from_store.setter
    def certificates_from_store(self, value: tuple[StoreName, StoreLocation]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AddCertificatesFromStore({format_enum(value[0])}, {format_enum(value[1])});')

    @property
    def certificates_from_file(self) -> NoReturn:
        raise TypeError("certificates_from_file is write-only")

    @certificates_from_file.setter
    def certificates_from_file(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AddCertificatesFromFile("{value}");')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[CertificateAuthorityCollectionOptions]) -> None:
        if certificate := kwargs.pop("certificate", None):
            if isinstance(certificate, bytes):
                # TODO: This will need X509Certificate2 certificate = X509CertificateLoader.LoadCertificate(certData);
                builder.write(f'\n    .AddCertificate(Convert.FromBase64String("{certificate.decode()}"))')
            else:
                builder.write(f'\n    .AddCertificate(File.ReadAllText("{certificate}"))')
        if certificates := kwargs.pop("certificates", None):
            for cert in certificates:
                if isinstance(cert, bytes):
                    builder.write(f'\n    .AddCertificate(Convert.FromBase64String("{cert.decode()}"))')
                else:
                    builder.write(f'\n    .AddCertificate(File.ReadAllText("{cert}"))')
        if certificates_from_store := kwargs.pop("certificates_from_store", None):
            store_name, store_location = certificates_from_store
            builder.write(f'\n    .AddCertificatesFromStore(StoreName.{store_name.value}, StoreLocation.{store_location.value})')
        if certificates_from_file := kwargs.pop("certificates_from_file", None):
            builder.write(f'\n    .AddCertificatesFromFile("{certificates_from_file}")')
        super().__init__(name=name, builder=builder, **kwargs)


class ConnectionStringResourceOptions(ResourceOptions, ResourceWithConnectionStringOptions, ResourceWithWaitSupportOptions, total=False):
    ...


class ConnectionStringResource(ResourceWithConnectionString, Resource):

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ConnectionStringResourceOptions]) -> None:
        super().__init__(name=name, builder=builder, **kwargs)


class ParameterResourceOptions(ResourceOptions, total=False):
    description: str | tuple[str, bool]


class ParameterResource(Resource):
    @property
    def description(self) -> NoReturn:
        raise TypeError("description is write-only")

    @description.setter
    def description(self, value: str | tuple[str, bool]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f"\n{self.name}.WithDescription(\"{value}\");")
        else:
            self._builder.write(f"\n{self.name}.WithDescription(\"{value[0]}\", {str(value[1]).lower()});")

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ParameterResourceOptions]) -> None:
        if description := kwargs.pop("description", None):
            if isinstance(description, str):
                builder.write(f"\n    .WithDescription(\"{description}\")")
            else:
                builder.write(f"\n    .WithDescription(\"{description[0]}\", {str(description[1]).lower()})")
        super().__init__(name, builder=builder, **kwargs)


class ProjectResourceOptions(ResourceOptions, ResourceWithEnvironmentOptions, ResourceWithArgsOptions, ResourceWithServiceDiscoveryOptions, ResourceWithWaitSupportOptions, ResourceWithProbesOptions,
    ComputeResourceOptions, ContainerFilesDestinationResourceOptions, total=False):
    disable_forwarded_headers: Literal[True]
    replicas: int


class ProjectResource(ResourceWithEnvironment, ResourceWithArgs, ResourceWithServiceDiscovery, ResourceWithWaitSupport, ResourceWithProbes,
    ComputeResource, ContainerFilesDestinationResource, Resource):
    @property
    def disable_forwarded_headers(self) -> NoReturn:
        raise TypeError("disable_forwarded_headers is write-only")

    @disable_forwarded_headers.setter
    def disable_forwarded_headers(self, value: Literal[True]) -> None:
        self._builder: StringIO
        self.name: str
        if value is True:
            self._builder.write(f"\n{self.name}.DisableForwardedHeaders();")

    @property
    def replicas(self) -> NoReturn:
        raise TypeError("replicas is write-only")

    @replicas.setter
    def replicas(self, value: int) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f"\n{self.name}.WithReplicas({value});")

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ProjectResourceOptions]) -> None:
        if disable_forwarded_headers := kwargs.pop("disable_forwarded_headers", None):
            if disable_forwarded_headers is True:
                builder.write(f"\n    .DisableForwardedHeaders()")
        if replicas := kwargs.pop("replicas", None):
            builder.write(f"\n    .WithReplicas({replicas})")
        super().__init__(name=name, builder=builder, **kwargs)


class ExecutableResourceOptions(ResourceOptions, ResourceWithEnvironmentOptions, ResourceWithEndpointsOptions, ResourceWithWaitSupportOptions, ResourceWithProbesOptions, ComputeResourceOptions, total=False):
    publish_as_dockerfile: Literal[True]
    command: str
    working_directory: str
    certificate_trust_scope: CertificateTrustScope
    developer_certificate_trust: bool
    certificate_authority_collection: CertificateAuthorityCollection


class ExecutableResource(ResourceWithEnvironment, ResourceWithArgs, ResourceWithEndpoints, ResourceWithWaitSupport, ResourceWithProbes, ComputeResource, Resource):
    @property
    def publish_as_dockerfile(self) -> NoReturn:
        raise TypeError("publish_as_dockerfile is write-only")

    @publish_as_dockerfile.setter
    def publish_as_dockerfile(self, value: Literal[True]) -> None:
        if value is True:
            self._builder: StringIO
            self.name: str
            self._builder.write(f'\n{self.name}.PublishAsDockerFile();')

    @property
    def command(self) -> NoReturn:
        raise TypeError("command is write-only")

    @command.setter
    def command(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCommand("{value}");')

    @property
    def working_directory(self) -> NoReturn:
        raise TypeError("working_directory is write-only")

    @working_directory.setter
    def working_directory(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithWorkingDirectory("{value}");')

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ExecutableResourceOptions]) -> None:
        if command := kwargs.pop("command", None):
            builder.write(f'\n    .WithCommand("{command}")')
        if working_directory := kwargs.pop("working_directory", None):
            builder.write(f'\n    .WithWorkingDirectory("{working_directory}")')
        if publish_as_dockerfile := kwargs.pop("publish_as_dockerfile", None):
            if publish_as_dockerfile is True:
                builder.write(f'\n    .PublishAsDockerFile()')
        super().__init__(name=name, builder=builder, **kwargs)


class ContainerFileSystemItem(TypedDict, total=False, extra_items=bool):
    group: int
    mode: Required[UnixFileMode]
    name: Required[str]
    owner: int


class ContainerFiles(TypedDict, total=False):
    destination_path: Required[str]
    entries: Required[Iterable[ContainerFileSystemItem]]
    default_owner: int
    default_group: int
    umask: UnixFileMode


class ContainerFilesFromSource(TypedDict, total=False):
    destination_path: Required[str]
    source_path: Required[str]
    default_owner: int
    default_group: int
    umask: UnixFileMode


class Volume(TypedDict, total=False):
    name: str
    target: Required[str]
    is_read_only: bool


class ContainerResourceOptions(ResourceOptions, ResourceWithEnvironmentOptions, ResourceWithArgsOptions, ResourceWithEndpointsOptions, ResourceWithWaitSupportOptions, ResourceWithProbesOptions,
    ComputeResourceOptions, total=False):
    publish_as_container: Literal[True]
    bind_mount: tuple[str, str] | tuple[str, str, bool]
    bind_mounts: Iterable[tuple[str, str] | tuple[str, str, bool]]
    build_arg: tuple[str, ParameterResource]
    build_args: Iterable[tuple[str, ParameterResource]]
    build_secret: tuple[str, ParameterResource]
    build_secrets: Iterable[tuple[str, ParameterResource]]
    container_files: ContainerFiles | ContainerFilesFromSource
    container_runtime_args: Iterable[str]
    container_name: str
    dockerfile: str | tuple[str, Mapping[str, str]]
    endpoint_proxy_support: bool
    entrypoint: str
    image: str | tuple[str, str]
    image_pull_policy: ImagePullPolicy
    image_registry: Literal[True] | str
    image_sha256: str
    image_tag: str
    lifetime: ContainerLifetime
    volume: Volume


class ContainerResource(ResourceWithEnvironment, ResourceWithArgs, ResourceWithEndpoints, ResourceWithWaitSupport, ResourceWithProbes,
    ComputeResource, Resource):
    @property
    def publish_as_container(self) -> NoReturn:
        raise TypeError("publish_as_container is write-only")

    @publish_as_container.setter
    def publish_as_container(self, value: Literal[True]) -> None:
        if value is True:
            self._builder: StringIO
            self.name: str
            self._builder.write(f'\n{self.name}.PublishAsContainer();')

    @property
    def bind_mount(self) -> NoReturn:
        raise TypeError("bind_mount is write-only")

    @bind_mount.setter
    def bind_mount(self, value: tuple[str, str] | tuple[str, str, bool]) -> None:
        self._builder: StringIO
        self.name: str
        if len(value) == 2:
            self._builder.write(f'\n{self.name}.WithBindMount("{value[0]}", "{value[1]}");')
        else:
            self._builder.write(f'\n{self.name}.WithBindMount("{value[0]}", "{value[1]}", {str(value[2]).lower()});')

    @property
    def bind_mounts(self) -> NoReturn:
        raise TypeError("bind_mounts is write-only")

    @bind_mounts.setter
    def bind_mounts(self, value: Iterable[tuple[str, str] | tuple[str, str, bool]]) -> None:
        self._builder: StringIO
        self.name: str
        for mount in value:
            if len(mount) == 2:
                self._builder.write(f'\n{self.name}.WithBindMount("{mount[0]}", "{mount[1]}");')
            else:
                self._builder.write(f'\n{self.name}.WithBindMount("{mount[0]}", "{mount[1]}", {str(mount[2]).lower()});')

    @property
    def build_arg(self) -> NoReturn:
        raise TypeError("build_arg is write-only")

    @build_arg.setter
    def build_arg(self, value: tuple[str, ParameterResource]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithBuildArg("{value[0]}", {value[1].name});')

    @property
    def build_args(self) -> NoReturn:
        raise TypeError("build_args is write-only")

    @build_args.setter
    def build_args(self, value: Iterable[tuple[str, ParameterResource]]) -> None:
        self._builder: StringIO
        self.name: str
        for arg in value:
            self._builder.write(f'\n{self.name}.WithBuildArg("{arg[0]}", {arg[1].name});')

    @property
    def build_secret(self) -> NoReturn:
        raise TypeError("build_secret is write-only")

    @build_secret.setter
    def build_secret(self, value: tuple[str, ParameterResource]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithBuildSecret("{value[0]}", {value[1].name});')

    @property
    def build_secrets(self) -> NoReturn:
        raise TypeError("build_secrets is write-only")

    @build_secrets.setter
    def build_secrets(self, value: Iterable[tuple[str, ParameterResource]]) -> None:
        self._builder: StringIO
        self.name: str
        for secret in value:
            self._builder.write(f'\n{self.name}.WithBuildSecret("{secret[0]}", {secret[1].name});')

    @property
    def container_files(self) -> NoReturn:
        raise TypeError("container_files is write-only")

    @container_files.setter
    def container_files(self, value: ContainerFiles | ContainerFilesFromSource) -> None:
        self._builder: StringIO
        self.name: str
        # TODO: Test this logic. Seesm suspect
        if "entries" in value:
            entries = value["entries"]
            destination_path = value["destination_path"]
            default_owner = value.get("default_owner", None)
            default_group = value.get("default_group", None)
            umask = value.get("umask", None)
            self._builder.write(f'\n{self.name}.WithContainerFiles("{destination_path}", new List<ContainerFileSystemItem>{{')
            for entry in entries:
                entry_str = f'new ContainerFileSystemItem{{ Name = "{entry["name"]}", Mode = (UnixFileMode){entry["mode"]}'
                if "owner" in entry:
                    entry_str += f', Owner = {entry["owner"]}'
                if "group" in entry:
                    entry_str += f', Group = {entry["group"]}'
                entry_str += ' }'
                self._builder.write(entry_str + ',')
            self._builder.write('}}')
            if default_owner is not None:
                self._builder.write(f', defaultOwner: {default_owner}')
            if default_group is not None:
                self._builder.write(f', defaultGroup: {default_group}')
            if umask is not None:
                self._builder.write(f', umask: (UnixFileMode){umask}')
            self._builder.write(');')
        elif "source_path" in value:
            source_path = value["source_path"]
            destination_path = value["destination_path"]
            default_owner = value.get("default_owner", None)
            default_group = value.get("default_group", None)
            umask = value.get("umask", None)
            self._builder.write(f'\n{self.name}.WithContainerFiles("{destination_path}", "{source_path}"')
            if default_owner is not None:
                self._builder.write(f', defaultOwner: {default_owner}')
            if default_group is not None:
                self._builder.write(f', defaultGroup: {default_group}')
            if umask is not None:
                self._builder.write(f', umask: (UnixFileMode){umask}')
            self._builder.write(');')

    @property
    def container_runtime_args(self) -> NoReturn:
        raise TypeError("container_runtime_args is write-only")

    @container_runtime_args.setter
    def container_runtime_args(self, value: Iterable[str]) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithContainerRuntimeArgs({format_string_array(value)});')

    @property
    def dockerfile(self) -> NoReturn:
        raise TypeError("dockerfile is write-only")

    @dockerfile.setter
    def dockerfile(self, value: str | tuple[str, Mapping[str, str]]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithDockerfile("{value}");')
        else:
            self._builder.write(f'\n{self.name}.WithDockerfile("{value[0]}", {get_nullable_from_map(value[1], "dockerfile_path")}, {get_nullable_from_map(value[1], "stage")});')

    @property
    def container_name(self) -> NoReturn:
        raise TypeError("container_name is write-only")

    @container_name.setter
    def container_name(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithContainerName({format_string(value)});')

    @property
    def endpoint_proxy_support(self) -> NoReturn:
        raise TypeError("endpoint_proxy_support is write-only")

    @endpoint_proxy_support.setter
    def endpoint_proxy_support(self, value: bool) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithEndpointProxySupport({format_bool(value)});')

    @property
    def entrypoint(self) -> NoReturn:
        raise TypeError("entrypoint is write-only")

    @entrypoint.setter
    def entrypoint(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithEntrypoint({format_string(value)});')

    @property
    def image(self) -> NoReturn:
        raise TypeError("image is write-only")

    @image.setter
    def image(self, value: str | tuple[str, str]) -> None:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithImage({format_string(value)});')
        else:
            self._builder.write(f'\n{self.name}.WithImage({format_string(value[0])}, {format_string(value[1])});')

    @property
    def image_pull_policy(self) -> NoReturn:
        raise TypeError("image_pull_policy is write-only")

    @image_pull_policy.setter
    def image_pull_policy(self, value: ImagePullPolicy) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImagePullPolicy({format_enum(value)});')

    @property
    def image_registry(self) -> NoReturn:
        raise TypeError("image_registry is write-only")

    @image_registry.setter
    def image_registry(self, value: Literal[True] | str) -> None:
        self._builder: StringIO
        self.name: str
        if value is True:
            self._builder.write(f'\n{self.name}.WithImageRegistry(null);')
        else:
            self._builder.write(f'\n{self.name}.WithImageRegistry("{value}");')

    @property
    def image_sha256(self) -> NoReturn:
        raise TypeError("image_sha256 is write-only")

    @image_sha256.setter
    def image_sha256(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImageSHA256("{value}");')

    @property
    def image_tag(self) -> NoReturn:
        raise TypeError("image_tag is write-only")

    @image_tag.setter
    def image_tag(self, value: str) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImageTag("{value}");')

    @property
    def lifetime(self) -> NoReturn:
        raise TypeError("lifetime is write-only")

    @lifetime.setter
    def lifetime(self, value: ContainerLifetime) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithLifetime(ContainerLifetime.{value.value});')

    @property
    def volume(self) -> NoReturn:
        raise TypeError("volume is write-only")

    @volume.setter
    def volume(self, value: Volume) -> None:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithVolume({get_nullable_from_map(value, "name")}, "{value["target"]}", {get_nullable_from_map(value, "is_read_only", False)});') # type: ignore

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ContainerResourceOptions]) -> None:
        if publish_as_container := kwargs.pop("publish_as_container", None):
            if publish_as_container is True:
                builder.write(f'\n    .PublishAsContainer()')
        if bind_mount := kwargs.pop("bind_mount", None):
            builder.write(f'\n    .WithBindMount(source: "{bind_mount[0]}", target: "{bind_mount[1]}", isReadOnly: {get_nullable_from_tuple(bind_mount, 2, False)} )')
        if bind_mounts := kwargs.pop("bind_mounts", None):
            for mount in bind_mounts:
                builder.write(f'\n    .WithBindMount(source: "{mount[0]}", target: "{mount[1]}", isReadOnly: {get_nullable_from_tuple(mount, 2, False)} )')
        if build_arg := kwargs.pop("build_arg", None):
            builder.write(f'\n    .WithBuildArg("{build_arg[0]}", {build_arg[1].name})')
        if build_args := kwargs.pop("build_args", None):
            for arg in build_args:
                builder.write(f'\n    .WithBuildArg("{arg[0]}", {arg[1].name})')
        if build_secret := kwargs.pop("build_secret", None):
            builder.write(f'\n    .WithBuildSecret("{build_secret[0]}", {build_secret[1].name})')
        if build_secrets := kwargs.pop("build_secrets", None):
            for secret in build_secrets:
                builder.write(f'\n    .WithBuildSecret("{secret[0]}", {secret[1].name})')
        if container_files := kwargs.pop("container_files", None):
            # TODO: Refactor
            if "entries" in container_files:
                entries = container_files["entries"]
                destination_path = container_files["destination_path"]
                default_owner = container_files.get("default_owner", None)
                default_group = container_files.get("default_group", None)
                umask = container_files.get("umask", None)
                builder.write(f'\n    .WithContainerFiles("{destination_path}", new List<ContainerFileSystemItem>{{')
                for entry in entries:
                    entry_str = f'new ContainerFileSystemItem{{ Name = "{entry["name"]}", Mode = (UnixFileMode){entry["mode"]}'
                    if "owner" in entry:
                        entry_str += f', Owner = {entry["owner"]}'
                    if "group" in entry:
                        entry_str += f', Group = {entry["group"]}'
                    entry_str += ' }'
                    builder.write(entry_str + ',')
                builder.write('}}')
                if default_owner is not None:
                    builder.write(f', defaultOwner: {default_owner}')
                if default_group is not None:
                    builder.write(f', defaultGroup: {default_group}')
                if umask is not None:
                    builder.write(f', umask: (UnixFileMode){umask}')
                builder.write(')')
            elif "source_path" in container_files:
                source_path = container_files["source_path"]
                destination_path = container_files["destination_path"]
                default_owner = container_files.get("default_owner", None)
                default_group = container_files.get("default_group", None)
                umask = container_files.get("umask", None)
                builder.write(f'\n    .WithContainerFiles("{destination_path}", "{source_path}"')
                if default_owner is not None:
                    builder.write(f', defaultOwner: {default_owner}')
                if default_group is not None:
                    builder.write(f', defaultGroup: {default_group}')
                if umask is not None:
                    builder.write(f', umask: (UnixFileMode){umask}')
                builder.write(')')
        if container_runtime_args := kwargs.pop("container_runtime_args", None):
            builder.write(f'\n    .WithContainerRuntimeArgs({format_string_array(container_runtime_args)})')
        if container_name := kwargs.pop("container_name", None):
            builder.write(f'\n    .WithContainerName({format_string(container_name)})')
        if dockerfile := kwargs.pop("dockerfile", None):
            if isinstance(dockerfile, str):
                builder.write(f'\n    .WithDockerfile({format_string(dockerfile)})')
            else:
                builder.write(f'\n    .WithDockerfile({format_string(dockerfile[0])}, {get_nullable_from_map(dockerfile[1], "dockerfile_path")}, {get_nullable_from_map(dockerfile[1], "stage")})')
        if endpoint_proxy_support := kwargs.pop("endpoint_proxy_support", None):
            builder.write(f'\n    .WithEndpointProxySupport({format_bool(endpoint_proxy_support)})')
        if entrypoint := kwargs.pop("entrypoint", None):
            builder.write(f'\n    .WithEntrypoint({format_string(entrypoint)})')
        if image := kwargs.pop("image", None):
            if isinstance(image, str):
                builder.write(f'\n    .WithImage(image: {format_string(image)})')
            else:
                builder.write(f'\n    .WithImage(image: {format_string(image[0])}, tag: {format_string(image[1])})')
        if image_pull_policy := kwargs.pop("image_pull_policy", None):
            builder.write(f'\n    .WithImagePullPolicy(pullPolicy: {format_enum(image_pull_policy)})')
        if image_registry := kwargs.pop("image_registry", None):
            if image_registry is True:
                builder.write(f'\n    .WithImageRegistry(null)')
            else:
                builder.write(f'\n    .WithImageRegistry({format_string(image_registry)})')
        if image_sha256 := kwargs.pop("image_sha256", None):
            builder.write(f'\n    .WithImageSHA256({format_string(image_sha256)})')
        if image_tag := kwargs.pop("image_tag", None):
            builder.write(f'\n    .WithImageTag({format_string(image_tag)})')
        if lifetime := kwargs.pop("lifetime", None):
            builder.write(f'\n    .WithLifetime({format_enum(lifetime)})')
        if volume := kwargs.pop("volume", None):
            builder.write(f'\n    .WithVolume({get_nullable_from_map(volume, "name")}, {format_string(volume["target"])}, {get_nullable_from_map(volume, "is_read_only", False)})')  # type: ignore
        super().__init__(name=name, builder=builder, **kwargs)


class CSharpAppResource(ProjectResource):
    ...
