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
    Required,
    Unpack,
    cast,
    Self,
    Annotated
)
from typing_extensions import TypedDict

from .._utils import (
    format_bool,
    format_byte_array,
    format_enum,
    format_string,
    format_string_array,
    get_nullable_value,
    get_nullable_from_map,
    get_nullable_from_tuple,
)
from .._annotations import experimental, Warnings
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
    dockerfile_base_image: Annotated[Literal[True] | Mapping[str, str], Warnings(experimental="ASPIREDOCKERFILEBUILDER001")]


class Resource:

    @property
    def package(self) -> Iterable[str]:
        return []

    def with_url(self, value: str | tuple[str, str]) -> Self:
        if isinstance(value, str):
            self._builder.write(f"\n{self.name}.WithUrl(\"{value}\");")
        else:
            self._builder.write(f"\n{self.name}.WithUrl(\"{value[0]}\", \"{value[1]}\");")
        return self

    def exclude_from_manifest(self) -> Self:
        self._builder.write(f"\n{self.name}.ExcludeFromManifest();")
        return self

    def exclude_from_mcp(self) -> Self:
        self._builder.write(f"\n{self.name}.ExcludeFromMcp();")
        return self

    def explicit_start(self) -> Self:
        self._builder.write(f"\n{self.name}.WithExplicitStart();")
        return self

    def with_health_check(self, value: str) -> Self:
        self._builder.write(f'\n{self.name}.WithHealthCheck("{value}");')
        return self

    def with_relationship(self, value: tuple[Resource, str]) -> Self:
        self._builder.write(f'\n{self.name}.WithRelationship({value[0].name}.Resource, "{value[1]}");')
        return self

    def with_reference_relationship(self, value: Resource) -> Self:
        self._builder.write(f'\n{self.name}.WithReferenceRelationship({value.name});')
        return self

    def with_parent_relationship(self, value: Resource) -> Self:
        self._builder.write(f'\n{self.name}.WithParentRelationship({value.name});')
        return self

    def with_child_relationship(self, value: Resource) -> Self:
        self._builder.write(f'\n{self.name}.WithChildRelationship({value.name});')
        return self

    def with_icon_name(self, value: str | tuple[str, IconVariant]) -> Self:
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithIconName("{value}");')
        else:
            self._builder.write(f'\n{self.name}.WithIconName("{value[0]}", IconVariant.{value[1].value});')
        return self

    def with_dockerfile_base_image(self, *, build_image: str | None = None, runtime_image: str | None = None) -> Self:
        with experimental(self._builder, "with_dockerfile_base_image", self.__class__, "ASPIREDOCKERFILEBUILDER001"):
            if build_image is None and runtime_image is None:
                self._builder.write(f'\n{self.name}.WithDockerfileBaseImage();')
            else:
                self._builder.write(f'\n{self.name}.WithDockerfileBaseImage({get_nullable_value(build_image)}, {get_nullable_value(runtime_image)});')
        return self

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
    def with_args(self, value: Iterable[str]) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithArgs({format_string_array(value)});')
        return self

    def with_certificate_trust_scope(self, value: CertificateTrustScope) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateTrustScope({format_enum(value)});')
        return self

    def with_developer_certificate_trust(self, value: bool) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust({format_bool(value)});')
        return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithArgsOptions]) -> None:
        if args := kwargs.pop("args", None):
            builder.write(f'\n    .WithArgs({format_string_array(args)})')
        if certificate_trust_scope := kwargs.pop("certificate_trust_scope", None):
            builder.write(f'\n    .WithCertificateTrustScope({format_enum(certificate_trust_scope)})')
        if developer_certificate_trust := kwargs.pop("developer_certificate_trust", None):
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
    http_probe: Annotated[HttpProbeConfiguration, Warnings(experimental="ASPIREPROBES001")]


class ResourceWithEndpoints:
    def as_http2_service(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AsHttp2Service();')
        return self

    def with_endpoint(self, **kwargs: Unpack[EndpointConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(kwargs, "port")
        target_port = get_nullable_from_map(kwargs, "target_port")
        scheme = get_nullable_from_map(kwargs, "scheme")
        name = get_nullable_from_map(kwargs, "name")
        env = get_nullable_from_map(kwargs, "env")
        is_proxied = get_nullable_from_map(kwargs, "is_proxied", True)
        is_external = get_nullable_from_map(kwargs, "is_external", False)
        protocol = get_nullable_from_map(kwargs, "protocol")
        self._builder.write(f'\n{self.name}.WithEndpoint({port}, {target_port}, {scheme}, {name}, {env}, {is_proxied}, {is_external}, {protocol});')
        return self

    def with_external_http_endpoints(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithExternalHttpEndpoints();')
        return self

    def with_http_endpoint(self, **kwargs: Unpack[EndpointConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(kwargs, "port")
        target_port = get_nullable_from_map(kwargs, "target_port")
        name = get_nullable_from_map(kwargs, "name")
        env = get_nullable_from_map(kwargs, "env")
        is_proxied = get_nullable_from_map(kwargs, "is_proxied", True)
        self._builder.write(f'\n{self.name}.WithHttpEndpoint({port}, {target_port}, {name}, {env}, {is_proxied});')
        return self

    def with_https_endpoint(self, **kwargs: Unpack[EndpointConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        port = get_nullable_from_map(kwargs, "port")
        target_port = get_nullable_from_map(kwargs, "target_port")
        name = get_nullable_from_map(kwargs, "name")
        env = get_nullable_from_map(kwargs, "env")
        is_proxied = get_nullable_from_map(kwargs, "is_proxied", True)
        self._builder.write(f'\n{self.name}.WithHttpsEndpoint({port}, {target_port}, {name}, {env}, {is_proxied});')
        return self

    def with_http_health_check(self, **kwargs: Unpack[HttpHealthCheckConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        path = get_nullable_from_map(kwargs, "path")
        status_code = get_nullable_from_map(kwargs, "status_code")
        endpoint_name = get_nullable_from_map(kwargs, "endpoint_name")
        self._builder.write(f'\n{self.name}.WithHttpHealthCheck({path}, {status_code}, {endpoint_name});')
        return self

    def with_http_probe(self, **kwargs: Unpack[HttpProbeConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        with experimental(self._builder, "with_http_probe", self.__class__, "ASPIREPROBES001"):
            path = get_nullable_from_map(kwargs, "path")
            initial_delay_seconds = get_nullable_from_map(kwargs, "initial_delay_seconds")
            period_seconds = get_nullable_from_map(kwargs, "period_seconds")
            timeout_seconds = get_nullable_from_map(kwargs, "timeout_seconds")
            failure_threshold = get_nullable_from_map(kwargs, "failure_threshold")
            success_threshold = get_nullable_from_map(kwargs, "success_threshold")
            endpoint_name = get_nullable_from_map(kwargs, "endpoint_name")
            self._builder.write(f'\n{self.name}.WithHttpProbe({format_enum(kwargs["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name});')
            return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithEndpointsOptions]) -> None:
        if kwargs.pop("http2_service", None) is True:
            builder.write(f'\n    .AsHttp2Service()')
        if endpoint := kwargs.pop("endpoint", None):
            port = get_nullable_from_map(endpoint, "port")
            target_port = get_nullable_from_map(endpoint, "target_port")
            scheme = get_nullable_from_map(endpoint, "scheme")
            name_ = get_nullable_from_map(endpoint, "name")
            env = get_nullable_from_map(endpoint, "env")
            is_proxied = get_nullable_from_map(endpoint, "is_proxied", True)
            is_external = get_nullable_from_map(endpoint, "is_external", False)
            protocol = get_nullable_from_map(endpoint, "protocol")
            builder.write(f'\n    .WithEndpoint({port}, {target_port}, {scheme}, {name_}, {env}, {is_proxied}, {is_external}, {protocol})')
        if kwargs.pop("external_http_endpoints", None) is True:
            builder.write(f'\n    .WithExternalHttpEndpoints()')
        if http_endpoint := kwargs.pop("http_endpoint", None):
            port = get_nullable_from_map(http_endpoint, "port")
            target_port = get_nullable_from_map(http_endpoint, "target_port")
            name_ = get_nullable_from_map(http_endpoint, "name")
            env = get_nullable_from_map(http_endpoint, "env")
            is_proxied = get_nullable_from_map(http_endpoint, "is_proxied", True)
            builder.write(f'\n    .WithHttpEndpoint({port}, {target_port}, {name_}, {env}, {is_proxied})')
        if https_endpoint := kwargs.pop("https_endpoint", None):
            port = get_nullable_from_map(https_endpoint, "port")
            target_port = get_nullable_from_map(https_endpoint, "target_port")
            name_ = get_nullable_from_map(https_endpoint, "name")
            env = get_nullable_from_map(https_endpoint, "env")
            is_proxied = get_nullable_from_map(https_endpoint, "is_proxied", True)
            builder.write(f'\n    .WithHttpsEndpoint({port}, {target_port}, {name_}, {env}, {is_proxied})')
        if http_health_check := kwargs.pop("http_health_check", None):
            path = get_nullable_from_map(http_health_check, "path")
            status_code = get_nullable_from_map(http_health_check, "status_code")
            endpoint_name = get_nullable_from_map(http_health_check, "endpoint_name")
            builder.write(f'\n    .WithHttpHealthCheck({path}, {status_code}, {endpoint_name})')
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


class ResourceWithProbesOptions(TypedDict, total=False):
    http_probe: Annotated[HttpProbeConfiguration, Warnings(experimental="ASPIREPROBES001")]


class ResourceWithProbes:
    def with_http_probe(self, **kwargs: Unpack[HttpProbeConfiguration]) -> Self:
        self._builder: StringIO
        self.name: str
        with experimental(self._builder, "with_http_probe", self.__class__, "ASPIREPROBES001"):
            path = get_nullable_from_map(kwargs, "path")
            initial_delay_seconds = get_nullable_from_map(kwargs, "initial_delay_seconds")
            period_seconds = get_nullable_from_map(kwargs, "period_seconds")
            timeout_seconds = get_nullable_from_map(kwargs, "timeout_seconds")
            failure_threshold = get_nullable_from_map(kwargs, "failure_threshold")
            success_threshold = get_nullable_from_map(kwargs, "success_threshold")
            endpoint_name = get_nullable_from_map(kwargs, "endpoint_name")
            self._builder.write(f'\n{self.name}.WithHttpProbe({format_enum(kwargs["type"])}, {path}, {initial_delay_seconds}, {period_seconds}, {timeout_seconds}, {failure_threshold}, {success_threshold}, {endpoint_name});')
        return self

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
    def with_connection_string_redirection(self, value: ResourceWithConnectionString) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithConnectionStringRedirection({value.name}.Resource);')
        return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithConnectionStringOptions]) -> None:
        if connection_string_redirection := kwargs.pop("connection_string_redirection", None):
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
    def with_environment(self, value: tuple[str, EndpointReference | ParameterResource | ResourceWithConnectionString | ExternalServiceResource | str | None]) -> Self:
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
        return self

    def with_reference(self, value: EndpointReference | ExternalServiceResource | ResourceWithServiceDiscovery | tuple[str, str] | ResourceWithConnectionString | Mapping[str, Any]) -> Self:
        self._builder: StringIO
        self.name: str
        # if isinstance(value, EndpointReference):  # TODO
        #     self._builder.write(f'\n{self.name}.WithReference({value});')  # TODO: fix EndpointReference string representation
        if isinstance(value, ExternalServiceResource):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')
        elif isinstance(value, ResourceWithServiceDiscovery):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')
        elif isinstance(value, tuple):
            self._builder.write(f'\n{self.name}.WithReference({format_string(value[0])}, {format_string(value[1])});')
        elif isinstance(value, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithReference({cast(Resource, value).name});')
        return self

    def with_otlp_exporter(self, value: OtlpProtocol | None = None) -> Self:
        self._builder: StringIO
        self.name: str
        if value is None:
            self._builder.write(f'\n{self.name}.WithOtlpExporter();')
        else:
            self._builder.write(f'\n{self.name}.WithOtlpExporter({format_enum(value)});')
        return self

    def with_reference_environment(self, value: ReferenceEnvironment) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithReferenceEnvironment({format_enum(value)});')
        return self

    def with_certificate_trust_scope(self, value: CertificateTrustScope) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateTrustScope({format_enum(value)});')
        return self

    def with_developer_certificate_trust(self, value: bool) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust({format_bool(value)});')
        return self

    def with_certificate_authority_collection(self, value: CertificateAuthorityCollection) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificateAuthorityCollection({value.name});')
        return self

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
    def wait_for(self, value: Resource | tuple[Resource, WaitBehavior]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitFor({value.name});')
        else:
            self._builder.write(f'\n{self.name}.WaitFor({value[0].name}, {format_enum(value[1])});')
        return self

    def wait_for_completion(self, value: Resource | tuple[Resource, int]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitForCompletion({value.name});')
        else:
            self._builder.write(f'\n{self.name}.WaitForCompletion({value[0].name}, {value[1]});')
        return self

    def wait_for_start(self, value: Resource | tuple[Resource, WaitBehavior]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, Resource):
            self._builder.write(f'\n{self.name}.WaitForStart({value.name});')
        else:
            self._builder.write(f'\n{self.name}.WaitForStart({value[0].name}, {format_enum(value[1])});')
        return self

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
    def with_compute_environment(self, value: ComputeEnvironmentResource) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithComputeEnvironment({cast(Resource, value).name});')
        return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ComputeResourceOptions]) -> None:
        if compute_environment := kwargs.pop("compute_environment", None):
            builder.write(f'\n    .WithComputeEnvironment({cast(Resource, compute_environment).name})')
        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance


class ResourceWithContainerFilesOptions(TypedDict, total=False):
    container_files_source: str
    clear_container_files_sources: Literal[True]


class ResourceWithContainerFiles:

    def add_container_files_source(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.AddContainerFilesSource({format_string(value)});')
        return self

    def clear_container_files_sources(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.ClearContainerFilesSources();')
        return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ResourceWithContainerFilesOptions]) -> None:
        if container_files_source := kwargs.pop("container_files_source", None):
            builder.write(f'\n    .AddContainerFilesSource({format_string(container_files_source)})')
        if kwargs.pop("clear_container_files_sources", None) is True:
            builder.write(f'\n    .ClearContainerFilesSources()')
        super().__init__(name=name, builder=builder, **kwargs)  # type: ignore Assumes multiple inheritance


class ContainerFilesDestinationResourceOptions(TypedDict, total=False):
    publish_with_container_files: tuple[ResourceWithContainerFiles, str]


class ContainerFilesDestinationResource:
    def publish_with_container_files(self, value: tuple[ResourceWithContainerFiles, str]) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.PublishWithContainerFiles({cast(Resource, value[0]).name}, {format_string(value[1])});')
        return self

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

    def with_certificate(self, value: bytes | str) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, bytes):
            self._builder.write(f'\n{self.name}.WithCertificate(X509CertificateLoader.LoadCertificate({format_byte_array(value)}));')
        else:
            self._builder.write(f'\n{self.name}.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("{value}"));')
        return self

    def with_certificates_from_store(self, store_name: StoreName, store_location: StoreLocation) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificatesFromStore({format_enum(store_name)}, {format_enum(store_location)});')
        return self

    def with_certificates_from_file(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCertificatesFromFile("{value}");')
        return self

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[CertificateAuthorityCollectionOptions]) -> None:
        if certificate := kwargs.pop("certificate", None):
            if isinstance(certificate, bytes):
                builder.write(f'\n    .WithCertificate(X509CertificateLoader.LoadCertificate({format_byte_array(certificate)}))')
            else:
                builder.write(f'\n    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("{certificate}"))')
        if certificates := kwargs.pop("certificates", None):
            for cert in certificates:
                if isinstance(cert, bytes):
                    builder.write(f'\n    .WithCertificate(X509CertificateLoader.LoadCertificate({format_byte_array(cert)}))')
                else:
                    builder.write(f'\n    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("{cert}"))')
        if certificates_from_store := kwargs.pop("certificates_from_store", None):
            store_name, store_location = certificates_from_store
            builder.write(f'\n    .WithCertificatesFromStore(StoreName.{store_name.value}, StoreLocation.{store_location.value})')
        if certificates_from_file := kwargs.pop("certificates_from_file", None):
            builder.write(f'\n    .WithCertificatesFromFile("{certificates_from_file}")')
        super().__init__(name=name, builder=builder, **kwargs)


class ConnectionStringResourceOptions(ResourceOptions, ResourceWithConnectionStringOptions, total=False):
    ...


class ConnectionStringResource(ResourceWithConnectionString, Resource):

    def __init__(self, name: str, builder: StringIO, **kwargs: Unpack[ConnectionStringResourceOptions]) -> None:
        super().__init__(name=name, builder=builder, **kwargs)


class ParameterResourceOptions(ResourceOptions, total=False):
    description: str | tuple[str, bool]


class ParameterResource(Resource):
    # TODO: Fix up all method signatures
    def with_description(self, value: str | tuple[str, bool]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f"\n{self.name}.WithDescription(\"{value}\");")
        else:
            self._builder.write(f"\n{self.name}.WithDescription(\"{value[0]}\", {str(value[1]).lower()});")
        return self

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

    def disable_forwarded_headers(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f"\n{self.name}.DisableForwardedHeaders();")
        return self

    def with_replicas(self, value: int) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f"\n{self.name}.WithReplicas({value});")
        return self

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

    def publish_as_dockerfile(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.PublishAsDockerFile();')
        return self

    def with_command(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithCommand("{value}");')
        return self

    def with_working_directory(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithWorkingDirectory("{value}");')
        return self

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
    endpoint_proxy_support: Annotated[bool, Warnings(experimental="ASPIREPROXYENDPOINTS001")]
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
    def publish_as_container(self) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.PublishAsContainer();')
        return self

    def with_bind_mount(self, value: tuple[str, str] | tuple[str, str, bool]) -> Self:
        self._builder: StringIO
        self.name: str
        if len(value) == 2:
            self._builder.write(f'\n{self.name}.WithBindMount("{value[0]}", "{value[1]}");')
        else:
            self._builder.write(f'\n{self.name}.WithBindMount("{value[0]}", "{value[1]}", {str(value[2]).lower()});')
        return self

    def with_build_arg(self, value: tuple[str, ParameterResource]) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithBuildArg("{value[0]}", {value[1].name});')
        return self

    def with_build_secret(self, value: tuple[str, ParameterResource]) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithBuildSecret("{value[0]}", {value[1].name});')
        return self

    def with_container_files(self, value: ContainerFiles | ContainerFilesFromSource) -> Self:
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
        return self

    def with_container_runtime_args(self, value: Iterable[str]) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithContainerRuntimeArgs({format_string_array(value)});')
        return self

    def with_dockerfile(self, value: str | tuple[str, Mapping[str, str]]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithDockerfile("{value}");')
        else:
            self._builder.write(f'\n{self.name}.WithDockerfile("{value[0]}", {get_nullable_from_map(value[1], "dockerfile_path")}, {get_nullable_from_map(value[1], "stage")});')
        return self

    def with_container_name(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithContainerName({format_string(value)});')
        return self

    def with_endpoint_proxy_support(self, value: bool) -> Self:
        self._builder: StringIO
        self.name: str
        with experimental(self._builder, "with_endpoint_proxy_support", self.__class__, "ASPIREPROXYENDPOINTS001"):
            self._builder.write(f'\n{self.name}.WithEndpointProxySupport({format_bool(value)});')
        return self

    def with_entrypoint(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithEntrypoint({format_string(value)});')
        return self

    def with_image(self, value: str | tuple[str, str]) -> Self:
        self._builder: StringIO
        self.name: str
        if isinstance(value, str):
            self._builder.write(f'\n{self.name}.WithImage({format_string(value)});')
        else:
            self._builder.write(f'\n{self.name}.WithImage({format_string(value[0])}, {format_string(value[1])});')
        return self

    def with_image_pull_policy(self, value: ImagePullPolicy) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImagePullPolicy({format_enum(value)});')
        return self

    def with_image_registry(self, value: str | None = None) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImageRegistry({get_nullable_value(value)});')
        return self

    def with_image_sha256(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImageSHA256({format_string(value)});')
        return self

    def with_image_tag(self, value: str) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithImageTag({format_string(value)});')
        return self

    def with_lifetime(self, value: ContainerLifetime) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithLifetime({format_enum(value)});')
        return self

    def with_volume(self, value: Volume) -> Self:
        self._builder: StringIO
        self.name: str
        self._builder.write(f'\n{self.name}.WithVolume({get_nullable_from_map(value, "name")}, "{value["target"]}", {get_nullable_from_map(value, "is_read_only", False)});') # type: ignore
        return self

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
