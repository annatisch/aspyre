#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#
#   This is a generated file. Any modifications may be overwritten.
#   -------------------------------------------------------------
from __future__ import annotations
from typing import Any, Unpack, Self, Protocol, Literal, Annotated, get_origin, get_args, get_type_hints, cast, overload, runtime_checkable, Required
from typing_extensions import TypedDict
from collections.abc import Iterable, Mapping
from types import UnionType
from io import StringIO
from pathlib import Path
from contextlib import contextmanager
from warnings import warn
from base64 import b64encode
from dataclasses import dataclass
from re import compile
from datetime import timedelta


__VERSION__ = "13.0.1.0"
_VALID_NAME = compile(r'^[a-zA-Z0-9-]+$')


def _valid_var_name(name: str) -> str:
    if not _VALID_NAME.match(name):
        raise ValueError(f"Invalid name '{name}'. Only alphanumeric characters and hyphens are allowed.")
    return name.replace("-", "_")


def _validate_type(arg: Any, expected_type: Any) -> bool:
    if get_origin(expected_type) is Iterable:
        item_type = get_args(expected_type)[0]
        if not isinstance(arg, Iterable):
            return False
        for item in arg:
            if not _validate_type(item, item_type):
                return False
    elif get_origin(expected_type) is Mapping:
        key_type, value_type = get_args(expected_type)
        if not isinstance(arg, Mapping):
            return False
        for key, value in arg.items():
            if not _validate_type(key, key_type):
                return False
            if not _validate_type(value, value_type):
                return False
    elif isinstance(arg, (tuple, Mapping)):
        return False
    elif get_origin(expected_type) is Literal:
        if arg not in get_args(expected_type):
            return False
    elif expected_type is None:
        if arg is not None:
            return False
    elif subtypes := get_args(expected_type):
        # This is probably a Union type
        return any([_validate_type(arg, subtype) for subtype in subtypes])
    elif not isinstance(arg, expected_type):
        return False
    return True


def _validate_tuple_types(args: Any, arg_types: tuple[Any, ...]) -> bool:
    if not isinstance(args, tuple):
        return False
    if len(args) != len(arg_types):
        return False
    for arg, expected_type in zip(args, arg_types):
        if not _validate_type(arg, expected_type):
            return False
    return True


def _validate_dict_types(args: Any, arg_types: Any) -> bool:
    if not isinstance(args, Mapping):
        return False
    type_hints = get_type_hints(arg_types, include_extras=True)
    for key, expected_type in type_hints.items():
        if get_origin(expected_type) is Required:
            expected_type = get_args(expected_type)[0]
            if key not in args:
                return False
        if key not in args:
            continue
        value = args[key]
        if not _validate_type(value, expected_type):
            return False
    return True


def _format_value(value: Any, default: Any = None) -> str:
    if value is None:
        if default is not None:
            return str(default)
        return "null"
    if isinstance(value, Resource):
        return f"{value.name}.Resource"
    return str(value)


def _format_string(value: Any, default: Any = None) -> str:
    if value is None:
        if default is not None:
            return _format_string(default)
        return "(string?)null"
    return f'"{value}"'


def _format_string_array(strings: Iterable[str] | None) -> str:
    if strings is None:
        return "null"
    formatted_items = ', '.join(_format_string(s) for s in strings)
    return f'new string[] {{ {formatted_items} }}'


def _format_byte_array(bytes_value: bytes) -> str:
    base64_str = b64encode(bytes_value).decode('utf-8')
    return f'Convert.FromBase64String("{base64_str}")'


def _format_enum(enum_type: str, enum_value: str | None, default: str | None = None) -> str:
    if enum_value is None:
        if default is not None:
            return _format_enum(enum_type, default)
        return "null"
    return f'{enum_type}.{enum_value}'


def _format_bool(value: bool | None, default: bool | None = None) -> str:
    if value is None:
        if default is not None:
            return _format_bool(default)
        return "null"
    return str(value).lower()


def _format_cert(value: bytes | str | Iterable[bytes | str] | None) -> str:
    if value is None:
        return "null"
    elif isinstance(value, (bytes, bytearray)):
        return f"X509CertificateLoader.LoadCertificate({_format_byte_array(value)})"
    elif isinstance(value, str):
        return f"X509CertificateLoader.LoadCertificateFromFile({_format_string(value)})"
    formatted_items = ', '.join(_format_cert(s) for s in cast(Iterable[str | bytes], value))
    return f'new List<X509Certificate2> {{ {formatted_items} }}'


@dataclass
class Warnings:
    experimental: str | None


class AspyreExperimentalWarning(Warning):
    '''Custom warning for experimental features in Aspire.'''


@contextmanager
def _experimental(builder: StringIO, arg_name: str, func_or_cls: str | type, code: str):
    if isinstance(func_or_cls, str):
        warn(
            f"The '{arg_name}' option in '{func_or_cls}' is for evaluation purposes only and is subject "
            f"to change or removal in future updates. (Code: {code})",
            category=AspyreExperimentalWarning,
        )
        builder.write(f"\n#pragma warning disable {code}")
        yield
        builder.write(f"\n#pragma warning restore {code}")
    else:
        warn(
            f"The '{arg_name}' method of '{func_or_cls.__name__}' is for evaluation purposes only and is subject "
            f"to change or removal in future updates. (Code: {code})",
            category=AspyreExperimentalWarning,
        )
        builder.write(f"\n#pragma warning disable {code}")
        yield
        builder.write(f"\n#pragma warning restore {code}")


@contextmanager
def _check_warnings(builder: StringIO, kwargs: Mapping[str, Any], annotations: Any, func_name: str):
    type_hints = get_type_hints(annotations, include_extras=True)
    for key in kwargs.keys():
        if get_origin(type_hint := type_hints.get(key)) is Annotated:
            annotated_warnings = cast(Warnings, get_args(type_hint)[1])
            if annotated_warnings.experimental:
                warn(
                    f"The '{key}' option in '{func_name}' is for evaluation purposes only and is subject to change"
                    f"or removal in future updates. (Code: {annotated_warnings.experimental})",
                    category=AspyreExperimentalWarning,
                )
                builder.write(f"\n#pragma warning disable {annotated_warnings.experimental}")
                yield
                builder.write(f"\n#pragma warning restore {annotated_warnings.experimental}")
                return
    yield


EntrypointType = Literal['Executable', 'Script', 'Module']

OtlpProtocol = Literal['Grpc', 'HttpProtobuf']

ReferenceEnvironmentInjectionFlags = Literal['None', 'ConnectionString', 'ConnectionProperties', 'ServiceDiscovery', 'Endpoints', 'All']

ProtocolType = Literal['Unknown', 'IP', 'IPv6HopByHopOptions', 'Unspecified', 'Icmp', 'Igmp', 'Ggp', 'IPv4', 'Tcp', 'Pup', 'Udp', 'Idp', 'IPv6', 'IPv6RoutingHeader', 'IPv6FragmentHeader', 'IPSecEncapsulatingSecurityPayload', 'IPSecAuthenticationHeader', 'IcmpV6', 'IPv6NoNextHeader', 'IPv6DestinationOptions', 'ND', 'Raw', 'Ipx', 'Spx', 'SpxII']

WaitBehavior = Literal['WaitOnResourceUnavailable', 'StopOnResourceUnavailable']

CertificateTrustScope = Literal['None', 'Append', 'Override', 'System']

IconVariant = Literal['Regular', 'Filled']

ProbeType = Literal['Startup', 'Readiness', 'Liveness']

ContainerLifetime = Literal['Session', 'Persistent']

ImagePullPolicy = Literal['Default', 'Always', 'Missing']

UnixFileMode = Literal['None', 'OtherExecute', 'OtherWrite', 'OtherRead', 'GroupExecute', 'GroupWrite', 'GroupRead', 'UserExecute', 'UserWrite', 'UserRead', 'StickyBit', 'SetGroup', 'SetUser']

StoreName = Literal['AddressBook', 'AuthRoot', 'CertificateAuthority', 'Disallowed', 'My', 'Root', 'TrustedPeople', 'TrustedPublisher']

StoreLocation = Literal['CurrentUser', 'LocalMachine']


class DockerfileBaseImageParameters(TypedDict, total=False):
    build_image: str
    runtime_image: str


class HttpHealthCheckParameters(TypedDict, total=False):
    path: str
    status_code: int


class Volume2Parameters(TypedDict, total=False):
    name: Required[str]
    target: Required[str]
    is_read_only: bool


class BindMountParameters(TypedDict, total=False):
    source: Required[str]
    target: Required[str]
    is_read_only: bool


class DockerfileParameters(TypedDict, total=False):
    context_path: Required[str]
    dockerfile_path: str
    stage: str


class ContainerCertificatePathsParameters(TypedDict, total=False):
    custom_certificates_destination: str
    default_certificate_bundle_paths: Iterable[str]
    default_certificate_dir_paths: Iterable[str]


class ContainerFilesParameters(TypedDict, total=False):
    destination_path: Required[str]
    source_path: Required[str]
    default_owner: int
    default_group: int
    umask: UnixFileMode


class Reference1Parameters(TypedDict, total=False):
    source: Required[ResourceWithConnectionString]
    connection_name: str
    optional: bool


class EndpointParameters(TypedDict, total=False):
    port: int
    target_port: int
    scheme: str
    name: str
    env: str
    is_proxied: bool
    is_external: bool
    protocol: ProtocolType


class HttpEndpointParameters(TypedDict, total=False):
    port: int
    target_port: int
    name: str
    env: str
    is_proxied: bool


class HttpsEndpointParameters(TypedDict, total=False):
    port: int
    target_port: int
    name: str
    env: str
    is_proxied: bool


class HttpCommandParameters(TypedDict, total=False):
    path: Required[str]
    display_name: Required[str]
    endpoint_name: str
    command_name: str


class HttpProbeParameters(TypedDict, total=False):
    type: Required[ProbeType]
    path: str
    initial_delay_seconds: int
    period_seconds: int
    timeout_seconds: int
    failure_threshold: int
    success_threshold: int
    endpoint_name: str


class DataVolumeParameters(TypedDict, total=False):
    name: str
    is_read_only: bool


class PipParameters(TypedDict, total=False):
    install: bool
    install_args: Iterable[str]


class UvParameters(TypedDict, total=False):
    install: bool
    args: Iterable[str]


class PersistenceParameters(TypedDict, total=False):
    interval: timedelta
    keys_changed_threshold: int


@runtime_checkable
class Resource(Protocol):
    """Protocol for Resource"""
    name: str

    @property
    def package(self) -> str: ...


    def with_dockerfile_base_image(self, *, build_image: str | None = None, runtime_image: str | None = None) -> Self:
        ...

    def with_url(self, url: str, /, *, display_text: str | None = None) -> Self:
        ...

    def exclude_from_manifest(self) -> Self:
        ...

    def with_explicit_start(self) -> Self:
        ...

    def with_health_check(self, key: str, /) -> Self:
        ...

    def with_relationship(self, resource: Resource, type: str, /) -> Self:
        ...

    def with_reference_relationship(self, resource: Resource, /) -> Self:
        ...

    def with_parent_relationship(self, parent: Resource, /) -> Self:
        ...

    def with_child_relationship(self, child: Resource, /) -> Self:
        ...

    def with_icon_name(self, icon_name: str, /, *, icon_variant: IconVariant = "Filled") -> Self:
        ...

    def exclude_from_mcp(self) -> Self:
        ...


@runtime_checkable
class ResourceWithConnectionString(Resource, Protocol):
    """Protocol for ResourceWithConnectionString"""

    def with_connection_string_redirection(self, resource: ResourceWithConnectionString, /) -> Self:
        ...


@runtime_checkable
class ResourceWithEndpoints(Resource, Protocol):
    """Protocol for ResourceWithEndpoints"""

    @overload
    def with_endpoint(self, *, port: int | None = None, target_port: int | None = None, scheme: str | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True, is_external: bool | None = None, protocol: ProtocolType | None = None) -> Self:
        ...
    @overload
    def with_endpoint(self, scheme: str | None, name: str | None, env: str | None, is_proxied: bool, /, *, port: int | None = None, target_port: int | None = None, is_external: bool | None = None) -> Self:
        ...
    def with_endpoint(self, *args, **kwargs) -> Self:
        ...

    def with_http_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        ...

    def with_https_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        ...

    def with_external_http_endpoints(self) -> Self:
        ...

    def as_http2_service(self) -> Self:
        ...

    def with_http_health_check(self, *, path: str | None = None, status_code: int | None = None, endpoint_name: str | None = None) -> Self:
        ...

    def with_http_command(self, path: str, display_name: str, /, *, endpoint_name: str | None = None, command_name: str | None = None) -> Self:
        ...

    def with_http_probe(self, type: ProbeType, /, *, path: str | None = None, initial_delay_seconds: int | None = None, period_seconds: int | None = None, timeout_seconds: int | None = None, failure_threshold: int | None = None, success_threshold: int | None = None, endpoint_name: str | None = None) -> Self:
        ...


@runtime_checkable
class ResourceWithEnvironment(Resource, Protocol):
    """Protocol for ResourceWithEnvironment"""

    @overload
    def with_otlp_exporter(self) -> Self:
        ...
    @overload
    def with_otlp_exporter(self, protocol: OtlpProtocol, /) -> Self:
        ...
    def with_otlp_exporter(self, *args, **kwargs) -> Self:
        ...

    @overload
    def with_env(self, name: str, value: str | None, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, parameter: ParameterResource, /) -> Self:
        ...
    @overload
    def with_env(self, env_var_name: str, resource: ResourceWithConnectionString, /) -> Self:
        ...
    def with_env(self, *args, **kwargs) -> Self:
        ...

    def with_reference_env(self, flags: ReferenceEnvironmentInjectionFlags, /) -> Self:
        ...

    @overload
    def with_reference(self, source: ResourceWithConnectionString, /, *, connection_name: str | None = None, optional: bool = False) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, /) -> Self:
        ...
    @overload
    def with_reference(self, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, name: str, /) -> Self:
        ...
    def with_reference(self, *args, **kwargs) -> Self:
        ...

    def with_certificate_authority_collection(self, certificate_authority_collection: CertificateAuthorityCollection, /) -> Self:
        ...

    def with_developer_certificate_trust(self, trust: bool, /) -> Self:
        ...

    def with_certificate_trust_scope(self, scope: CertificateTrustScope, /) -> Self:
        ...


@runtime_checkable
class ResourceWithArgs(Resource, Protocol):
    """Protocol for ResourceWithArgs"""

    def with_args(self, args: Iterable[str], /) -> Self:
        ...

    def with_certificate_authority_collection(self, certificate_authority_collection: CertificateAuthorityCollection, /) -> Self:
        ...

    def with_developer_certificate_trust(self, trust: bool, /) -> Self:
        ...

    def with_certificate_trust_scope(self, scope: CertificateTrustScope, /) -> Self:
        ...


@runtime_checkable
class ResourceWithServiceDiscovery(ResourceWithEndpoints, Resource, Protocol):
    """Protocol for ResourceWithServiceDiscovery"""


@runtime_checkable
class ContainerFilesDestinationResource(Resource, Protocol):
    """Protocol for ContainerFilesDestinationResource"""

    def publish_with_container_files(self, source: ResourceWithContainerFiles, destination_path: str, /) -> Self:
        ...


@runtime_checkable
class ResourceWithContainerFiles(Resource, Protocol):
    """Protocol for ResourceWithContainerFiles"""

    def with_container_files_source(self, source_path: str, /) -> Self:
        ...

    def clear_container_files_sources(self) -> Self:
        ...


@runtime_checkable
class ResourceWithWaitSupport(Resource, Protocol):
    """Protocol for ResourceWithWaitSupport"""

    @overload
    def wait_for(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for(self, *args, **kwargs) -> Self:
        ...

    @overload
    def wait_for_start(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for_start(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for_start(self, *args, **kwargs) -> Self:
        ...

    def wait_for_completion(self, dependency: Resource, /, *, exit_code: int = 0) -> Self:
        ...


@runtime_checkable
class ComputeResource(Resource, Protocol):
    """Protocol for ComputeResource"""

    def with_compute_env(self, compute_env_resource: ComputeEnvironmentResource, /) -> Self:
        ...


@runtime_checkable
class ComputeEnvironmentResource(Resource, Protocol):
    """Protocol for ComputeEnvironmentResource"""


@runtime_checkable
class ResourceWithProbes(Resource, Protocol):
    """Protocol for ResourceWithProbes"""

    def with_http_probe(self, type: ProbeType, /, *, path: str | None = None, initial_delay_seconds: int | None = None, period_seconds: int | None = None, timeout_seconds: int | None = None, failure_threshold: int | None = None, success_threshold: int | None = None, endpoint_name: str | None = None) -> Self:
        ...


class _BaseResourceOptions(TypedDict, total=False):
    """Options for Resource base class."""
    dockerfile_base_image: Annotated[DockerfileBaseImageParameters | Literal[True], Warnings(experimental="ASPIREDOCKERFILEBUILDER001")]
    url: str | tuple[str, str]
    exclude_from_manifest: Literal[True]
    explicit_start: Literal[True]
    health_check: str
    relationship: tuple[Resource, str]
    reference_relationship: Resource
    parent_relationship: Resource
    child_relationship: Resource
    icon_name: str | tuple[str, IconVariant]
    exclude_from_mcp: Literal[True]


class _BaseResource:
    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[_BaseResourceOptions]) -> None:
        if _dockerfile_base_image := kwargs.pop("dockerfile_base_image", None):
            if _validate_dict_types(_dockerfile_base_image, DockerfileBaseImageParameters):
                build_image = cast(DockerfileBaseImageParameters, _dockerfile_base_image).get("build_image")
                runtime_image = cast(DockerfileBaseImageParameters, _dockerfile_base_image).get("runtime_image")
                __builder.write(f'\n    .WithDockerfileBaseImage(buildImage: {_format_string(build_image, None)}, runtimeImage: {_format_string(runtime_image, None)})')
            elif _dockerfile_base_image is True:
                __builder.write(f'\n    .WithDockerfileBaseImage()')
            else:
                raise TypeError("Invalid type for option 'dockerfile_base_image'")
        if _url := kwargs.pop("url", None):
            if _validate_type(_url, str):
                url = cast(str, _url)
                display_text = None
                __builder.write(f'\n    .WithUrl(url: {_format_string(url, None)}, displayText: {_format_string(display_text, None)})')
            elif _validate_tuple_types(_url, (str, str)):
                url, display_text = cast(tuple[str, str], _url)
                __builder.write(f'\n    .WithUrl(url: {_format_string(url, None)}, displayText: {_format_string(display_text, None)})')
            else:
                raise TypeError("Invalid type for option 'url'")
        if _exclude_from_manifest := kwargs.pop("exclude_from_manifest", None):
            if _exclude_from_manifest is True:
                __builder.write(f'\n    .ExcludeFromManifest()')
            else:
                raise TypeError("Invalid type for option 'exclude_from_manifest'")
        if _explicit_start := kwargs.pop("explicit_start", None):
            if _explicit_start is True:
                __builder.write(f'\n    .WithExplicitStart()')
            else:
                raise TypeError("Invalid type for option 'explicit_start'")
        if _health_check := kwargs.pop("health_check", None):
            if _validate_type(_health_check, str):
                key = cast(str, _health_check)
                __builder.write(f'\n    .WithHealthCheck(key: {_format_string(key, None)})')
            else:
                raise TypeError("Invalid type for option 'health_check'")
        if _relationship := kwargs.pop("relationship", None):
            if _validate_tuple_types(_relationship, (Resource, str)):
                resource, type, = cast(tuple[Resource, str], _relationship)
                __builder.write(f'\n    .WithRelationship(resource: {_format_value(resource, None)}, type: {_format_string(type, None)})')
            else:
                raise TypeError("Invalid type for option 'relationship'")
        if _reference_relationship := kwargs.pop("reference_relationship", None):
            if _validate_type(_reference_relationship, Resource):
                resource = cast(Resource, _reference_relationship)
                __builder.write(f'\n    .WithReferenceRelationship(resource: {_format_value(resource, None)})')
            else:
                raise TypeError("Invalid type for option 'reference_relationship'")
        if _parent_relationship := kwargs.pop("parent_relationship", None):
            if _validate_type(_parent_relationship, Resource):
                parent = cast(Resource, _parent_relationship)
                __builder.write(f'\n    .WithParentRelationship(parent: {parent.name})')
            else:
                raise TypeError("Invalid type for option 'parent_relationship'")
        if _child_relationship := kwargs.pop("child_relationship", None):
            if _validate_type(_child_relationship, Resource):
                child = cast(Resource, _child_relationship)
                __builder.write(f'\n    .WithChildRelationship(child: {child.name})')
            else:
                raise TypeError("Invalid type for option 'child_relationship'")
        if _icon_name := kwargs.pop("icon_name", None):
            if _validate_type(_icon_name, str):
                icon_name = cast(str, _icon_name)
                icon_variant = None
                __builder.write(f'\n    .WithIconName(iconName: {_format_string(icon_name, None)}, iconVariant: {_format_enum("IconVariant", icon_variant, "Filled")})')
            elif _validate_tuple_types(_icon_name, (str, IconVariant)):
                icon_name, icon_variant = cast(tuple[str, IconVariant], _icon_name)
                __builder.write(f'\n    .WithIconName(iconName: {_format_string(icon_name, None)}, iconVariant: {_format_enum("IconVariant", icon_variant, "Filled")})')
            else:
                raise TypeError("Invalid type for option 'icon_name'")
        if _exclude_from_mcp := kwargs.pop("exclude_from_mcp", None):
            if _exclude_from_mcp is True:
                __builder.write(f'\n    .ExcludeFromMcp()')
            else:
                raise TypeError("Invalid type for option 'exclude_from_mcp'")
        self.name = __name
        self._builder = __builder
        self._builder.write(";")
        if kwargs:
            raise TypeError(f"Unexpected keyword arguments: {list(kwargs.keys())}")


    def with_dockerfile_base_image(self, *, build_image: str | None = None, runtime_image: str | None = None) -> Self:
        if _validate_tuple_types((build_image, runtime_image), (str | None, str | None)):
            with _experimental(self._builder, "with_dockerfile_base_image", self.__class__, "ASPIREDOCKERFILEBUILDER001"):
                self._builder.write(f'\n{self.name}.WithDockerfileBaseImage(buildImage: {_format_string(build_image, None)}, runtimeImage: {_format_string(runtime_image, None)});')
                return self
        else:
            raise TypeError("No matching overload found.")

    def with_url(self, url: str, /, *, display_text: str | None = None) -> Self:
        if _validate_tuple_types((url, display_text), (str, str | None)):
            self._builder.write(f'\n{self.name}.WithUrl(url: {_format_string(url, None)}, displayText: {_format_string(display_text, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def exclude_from_manifest(self) -> Self:
        self._builder.write(f'\n{self.name}.ExcludeFromManifest();')
        return self

    def with_explicit_start(self) -> Self:
        self._builder.write(f'\n{self.name}.WithExplicitStart();')
        return self

    def with_health_check(self, key: str, /) -> Self:
        if _validate_type(key, str):
            self._builder.write(f'\n{self.name}.WithHealthCheck(key: {_format_string(key, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_relationship(self, resource: Resource, type: str, /) -> Self:
        if _validate_tuple_types((resource, type, ), (Resource, str)):
            self._builder.write(f'\n{self.name}.WithRelationship(resource: {_format_value(resource, None)}, type: {_format_string(type, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_reference_relationship(self, resource: Resource, /) -> Self:
        if _validate_type(resource, Resource):
            self._builder.write(f'\n{self.name}.WithReferenceRelationship(resource: {_format_value(resource, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_parent_relationship(self, parent: Resource, /) -> Self:
        if _validate_type(parent, Resource):
            self._builder.write(f'\n{self.name}.WithParentRelationship(parent: {parent.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_child_relationship(self, child: Resource, /) -> Self:
        if _validate_type(child, Resource):
            self._builder.write(f'\n{self.name}.WithChildRelationship(child: {child.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_icon_name(self, icon_name: str, /, *, icon_variant: IconVariant = "Filled") -> Self:
        if _validate_tuple_types((icon_name, icon_variant), (str, IconVariant | Literal["Filled"])):
            self._builder.write(f'\n{self.name}.WithIconName(iconName: {_format_string(icon_name, None)}, iconVariant: {_format_enum("IconVariant", icon_variant, "Filled")});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def exclude_from_mcp(self) -> Self:
        self._builder.write(f'\n{self.name}.ExcludeFromMcp();')
        return self


class ConnectionStringResourceOptions(_BaseResourceOptions, total=False):
    """Options for ConnectionStringResource"""
    connection_string_redirection: ResourceWithConnectionString
    wait_for: Resource | tuple[Resource, WaitBehavior]
    wait_for_start: Resource | tuple[Resource, WaitBehavior]
    wait_for_completion: Resource | tuple[Resource, int]


class ConnectionStringResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ConnectionStringResourceOptions]) -> None:
        if _connection_string_redirection := kwargs.pop("connection_string_redirection", None):
            if _validate_type(_connection_string_redirection, ResourceWithConnectionString):
                resource = cast(ResourceWithConnectionString, _connection_string_redirection)
                __builder.write(f'\n    .WithConnectionStringRedirection(resource: {_format_value(resource, None)})')
            else:
                raise TypeError("Invalid type for option 'connection_string_redirection'")
        if _wait_for := kwargs.pop("wait_for", None):
            if _validate_type(_wait_for, Resource):
                dependency = cast(Resource, _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for'")
        if _wait_for_start := kwargs.pop("wait_for_start", None):
            if _validate_type(_wait_for_start, Resource):
                dependency = cast(Resource, _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for_start, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_start'")
        if _wait_for_completion := kwargs.pop("wait_for_completion", None):
            if _validate_type(_wait_for_completion, Resource):
                dependency = cast(Resource, _wait_for_completion)
                exit_code = None
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            elif _validate_tuple_types(_wait_for_completion, (Resource, int)):
                dependency, exit_code = cast(tuple[Resource, int], _wait_for_completion)
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_completion'")
        super().__init__(__name, __builder, **kwargs)

    def with_connection_string_redirection(self, resource: ResourceWithConnectionString, /) -> Self:
        if _validate_type(resource, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithConnectionStringRedirection(resource: {_format_value(resource, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for_start(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for_start(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for_start(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def wait_for_completion(self, dependency: Resource, /, *, exit_code: int = 0) -> Self:
        if _validate_tuple_types((dependency, exit_code), (Resource, int | Literal[0])):
            self._builder.write(f'\n{self.name}.WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class ExternalServiceResourceOptions(_BaseResourceOptions, total=False):
    """Options for ExternalServiceResource"""
    http_health_check: HttpHealthCheckParameters | Literal[True]


class ExternalServiceResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ExternalServiceResourceOptions]) -> None:
        if _http_health_check := kwargs.pop("http_health_check", None):
            if _validate_dict_types(_http_health_check, HttpHealthCheckParameters):
                path = cast(HttpHealthCheckParameters, _http_health_check).get("path")
                status_code = cast(HttpHealthCheckParameters, _http_health_check).get("status_code")
                __builder.write(f'\n    .WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)})')
            elif _http_health_check is True:
                __builder.write(f'\n    .WithHttpHealthCheck()')
            else:
                raise TypeError("Invalid type for option 'http_health_check'")
        super().__init__(__name, __builder, **kwargs)

    def with_http_health_check(self, *, path: str | None = None, status_code: int | None = None) -> Self:
        if _validate_tuple_types((path, status_code), (str | None, int | None)):
            self._builder.write(f'\n{self.name}.WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class CertificateAuthorityCollectionOptions(_BaseResourceOptions, total=False):
    """Options for CertificateAuthorityCollection"""
    certificate: str | bytes
    certificates: Iterable[str | bytes]
    certificates_from_store: tuple[StoreName, StoreLocation]
    certificates_from_file: str


class CertificateAuthorityCollection(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[CertificateAuthorityCollectionOptions]) -> None:
        if _certificate := kwargs.pop("certificate", None):
            if _validate_type(_certificate, str | bytes):
                certificate = cast(str | bytes, _certificate)
                __builder.write(f'\n    .WithCertificate(certificate: {_format_cert(certificate)})')
            else:
                raise TypeError("Invalid type for option 'certificate'")
        if _certificates := kwargs.pop("certificates", None):
            if _validate_type(_certificates, Iterable[str | bytes]):
                certificates = cast(Iterable[str | bytes], _certificates)
                __builder.write(f'\n    .WithCertificates(certificates: {_format_cert(certificates)})')
            else:
                raise TypeError("Invalid type for option 'certificates'")
        if _certificates_from_store := kwargs.pop("certificates_from_store", None):
            if _validate_tuple_types(_certificates_from_store, (StoreName, StoreLocation)):
                store_name, store_location, = cast(tuple[StoreName, StoreLocation], _certificates_from_store)
                __builder.write(f'\n    .WithCertificatesFromStore(storeName: {_format_enum("StoreName", store_name, None)}, storeLocation: {_format_enum("StoreLocation", store_location, None)})')
            else:
                raise TypeError("Invalid type for option 'certificates_from_store'")
        if _certificates_from_file := kwargs.pop("certificates_from_file", None):
            if _validate_type(_certificates_from_file, str):
                pem_file_path = cast(str, _certificates_from_file)
                __builder.write(f'\n    .WithCertificatesFromFile(pemFilePath: {_format_string(pem_file_path, None)})')
            else:
                raise TypeError("Invalid type for option 'certificates_from_file'")
        super().__init__(__name, __builder, **kwargs)

    def with_certificate(self, certificate: str | bytes, /) -> Self:
        if _validate_type(certificate, str | bytes):
            self._builder.write(f'\n{self.name}.WithCertificate(certificate: {_format_cert(certificate)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificates(self, certificates: Iterable[str | bytes], /) -> Self:
        if _validate_type(certificates, Iterable[str | bytes]):
            self._builder.write(f'\n{self.name}.WithCertificates(certificates: {_format_cert(certificates)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificates_from_store(self, store_name: StoreName, store_location: StoreLocation, /) -> Self:
        if _validate_tuple_types((store_name, store_location, ), (StoreName, StoreLocation)):
            self._builder.write(f'\n{self.name}.WithCertificatesFromStore(storeName: {_format_enum("StoreName", store_name, None)}, storeLocation: {_format_enum("StoreLocation", store_location, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificates_from_file(self, pem_file_path: str, /) -> Self:
        if _validate_type(pem_file_path, str):
            self._builder.write(f'\n{self.name}.WithCertificatesFromFile(pemFilePath: {_format_string(pem_file_path, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class ContainerResourceOptions(_BaseResourceOptions, total=False):
    """Options for ContainerResource"""
    volume: str | tuple[str, str] | Volume2Parameters
    bind_mount: tuple[str, str] | BindMountParameters
    entrypoint: str
    image_tag: str
    image_registry: str
    image: str | tuple[str, str]
    image_sha256: str
    container_runtime_args: Iterable[str]
    lifetime: ContainerLifetime
    image_pull_policy: ImagePullPolicy
    publish_as_container: Literal[True]
    dockerfile: str | DockerfileParameters
    container_name: str
    build_arg: tuple[str, ParameterResource]
    build_secret: tuple[str, ParameterResource]
    container_certificate_paths: ContainerCertificatePathsParameters | Literal[True]
    container_files: tuple[str, str] | ContainerFilesParameters
    endpoint_proxy_support: Annotated[bool, Warnings(experimental="ASPIREPROXYENDPOINTS001")]
    otlp_exporter: Literal[True] | OtlpProtocol
    env: tuple[str, str] | tuple[str, ExternalServiceResource] | tuple[str, ParameterResource] | tuple[str, ResourceWithConnectionString]
    args: Iterable[str]
    reference_env: ReferenceEnvironmentInjectionFlags
    reference: ResourceWithConnectionString | Reference1Parameters | ResourceWithServiceDiscovery | ExternalServiceResource | tuple[ResourceWithServiceDiscovery, str]
    endpoint: EndpointParameters | Literal[True]
    http_endpoint: HttpEndpointParameters | Literal[True]
    https_endpoint: HttpsEndpointParameters | Literal[True]
    external_http_endpoints: Literal[True]
    as_http2_service: Literal[True]
    wait_for: Resource | tuple[Resource, WaitBehavior]
    wait_for_start: Resource | tuple[Resource, WaitBehavior]
    wait_for_completion: Resource | tuple[Resource, int]
    http_health_check: HttpHealthCheckParameters | Literal[True]
    http_command: tuple[str, str] | HttpCommandParameters
    certificate_authority_collection: CertificateAuthorityCollection
    developer_certificate_trust: bool
    certificate_trust_scope: CertificateTrustScope
    compute_env: ComputeEnvironmentResource
    http_probe: Annotated[ProbeType | HttpProbeParameters, Warnings(experimental="ASPIREPROBES001")]


class ContainerResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ContainerResourceOptions]) -> None:
        if _volume := kwargs.pop("volume", None):
            if _validate_type(_volume, str):
                target = cast(str, _volume)
                __builder.write(f'\n    .WithVolume(target: {_format_string(target, None)})')
            elif _validate_tuple_types(_volume, (str, str)):
                name, target, = cast(tuple[str, str], _volume)
                is_read_only = None
                __builder.write(f'\n    .WithVolume(name: {_format_string(name, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _validate_dict_types(_volume, Volume2Parameters):
                name = cast(Volume2Parameters, _volume)["name"]
                target = cast(Volume2Parameters, _volume)["target"]
                is_read_only = cast(Volume2Parameters, _volume).get("is_read_only")
                __builder.write(f'\n    .WithVolume(name: {_format_string(name, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            else:
                raise TypeError("Invalid type for option 'volume'")
        if _bind_mount := kwargs.pop("bind_mount", None):
            if _validate_tuple_types(_bind_mount, (str, str)):
                source, target, = cast(tuple[str, str], _bind_mount)
                is_read_only = None
                __builder.write(f'\n    .WithBindMount(source: {_format_string(source, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _validate_dict_types(_bind_mount, BindMountParameters):
                source = cast(BindMountParameters, _bind_mount)["source"]
                target = cast(BindMountParameters, _bind_mount)["target"]
                is_read_only = cast(BindMountParameters, _bind_mount).get("is_read_only")
                __builder.write(f'\n    .WithBindMount(source: {_format_string(source, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            else:
                raise TypeError("Invalid type for option 'bind_mount'")
        if _entrypoint := kwargs.pop("entrypoint", None):
            if _validate_type(_entrypoint, str):
                entrypoint = cast(str, _entrypoint)
                __builder.write(f'\n    .WithEntrypoint(entrypoint: {_format_string(entrypoint, None)})')
            else:
                raise TypeError("Invalid type for option 'entrypoint'")
        if _image_tag := kwargs.pop("image_tag", None):
            if _validate_type(_image_tag, str):
                tag = cast(str, _image_tag)
                __builder.write(f'\n    .WithImageTag(tag: {_format_string(tag, None)})')
            else:
                raise TypeError("Invalid type for option 'image_tag'")
        if _image_registry := kwargs.pop("image_registry", None):
            if _validate_type(_image_registry, str):
                registry = cast(str, _image_registry)
                __builder.write(f'\n    .WithImageRegistry(registry: {_format_string(registry, None)})')
            else:
                raise TypeError("Invalid type for option 'image_registry'")
        if _image := kwargs.pop("image", None):
            if _validate_type(_image, str):
                image = cast(str, _image)
                tag = None
                __builder.write(f'\n    .WithImage(image: {_format_string(image, None)}, tag: {_format_string(tag, None)})')
            elif _validate_tuple_types(_image, (str, str)):
                image, tag = cast(tuple[str, str], _image)
                __builder.write(f'\n    .WithImage(image: {_format_string(image, None)}, tag: {_format_string(tag, None)})')
            else:
                raise TypeError("Invalid type for option 'image'")
        if _image_sha256 := kwargs.pop("image_sha256", None):
            if _validate_type(_image_sha256, str):
                sha256 = cast(str, _image_sha256)
                __builder.write(f'\n    .WithImageSHA256(sha256: {_format_string(sha256, None)})')
            else:
                raise TypeError("Invalid type for option 'image_sha256'")
        if _container_runtime_args := kwargs.pop("container_runtime_args", None):
            if _validate_type(_container_runtime_args, Iterable[str]):
                args = cast(Iterable[str], _container_runtime_args)
                __builder.write(f'\n    .WithContainerRuntimeArgs(args: {_format_string_array(args)})')
            else:
                raise TypeError("Invalid type for option 'container_runtime_args'")
        if _lifetime := kwargs.pop("lifetime", None):
            if _validate_type(_lifetime, ContainerLifetime):
                lifetime = cast(ContainerLifetime, _lifetime)
                __builder.write(f'\n    .WithLifetime(lifetime: {_format_enum("ContainerLifetime", lifetime, None)})')
            else:
                raise TypeError("Invalid type for option 'lifetime'")
        if _image_pull_policy := kwargs.pop("image_pull_policy", None):
            if _validate_type(_image_pull_policy, ImagePullPolicy):
                pull_policy = cast(ImagePullPolicy, _image_pull_policy)
                __builder.write(f'\n    .WithImagePullPolicy(pullPolicy: {_format_enum("ImagePullPolicy", pull_policy, None)})')
            else:
                raise TypeError("Invalid type for option 'image_pull_policy'")
        if _publish_as_container := kwargs.pop("publish_as_container", None):
            if _publish_as_container is True:
                __builder.write(f'\n    .PublishAsContainer()')
            else:
                raise TypeError("Invalid type for option 'publish_as_container'")
        if _dockerfile := kwargs.pop("dockerfile", None):
            if _validate_type(_dockerfile, str):
                context_path = cast(str, _dockerfile)
                dockerfile_path = None
                stage = None
                __builder.write(f'\n    .WithDockerfile(contextPath: {_format_string(context_path, None)}, dockerfilePath: {_format_string(dockerfile_path, None)}, stage: {_format_string(stage, None)})')
            elif _validate_dict_types(_dockerfile, DockerfileParameters):
                context_path = cast(DockerfileParameters, _dockerfile)["context_path"]
                dockerfile_path = cast(DockerfileParameters, _dockerfile).get("dockerfile_path")
                stage = cast(DockerfileParameters, _dockerfile).get("stage")
                __builder.write(f'\n    .WithDockerfile(contextPath: {_format_string(context_path, None)}, dockerfilePath: {_format_string(dockerfile_path, None)}, stage: {_format_string(stage, None)})')
            else:
                raise TypeError("Invalid type for option 'dockerfile'")
        if _container_name := kwargs.pop("container_name", None):
            if _validate_type(_container_name, str):
                name = cast(str, _container_name)
                __builder.write(f'\n    .WithContainerName(name: {_format_string(name, None)})')
            else:
                raise TypeError("Invalid type for option 'container_name'")
        if _build_arg := kwargs.pop("build_arg", None):
            if _validate_tuple_types(_build_arg, (str, ParameterResource)):
                name, value, = cast(tuple[str, ParameterResource], _build_arg)
                __builder.write(f'\n    .WithBuildArg(name: {_format_string(name, None)}, value: {value.name})')
            else:
                raise TypeError("Invalid type for option 'build_arg'")
        if _build_secret := kwargs.pop("build_secret", None):
            if _validate_tuple_types(_build_secret, (str, ParameterResource)):
                name, value, = cast(tuple[str, ParameterResource], _build_secret)
                __builder.write(f'\n    .WithBuildSecret(name: {_format_string(name, None)}, value: {value.name})')
            else:
                raise TypeError("Invalid type for option 'build_secret'")
        if _container_certificate_paths := kwargs.pop("container_certificate_paths", None):
            if _validate_dict_types(_container_certificate_paths, ContainerCertificatePathsParameters):
                custom_certificates_destination = cast(ContainerCertificatePathsParameters, _container_certificate_paths).get("custom_certificates_destination")
                default_certificate_bundle_paths = cast(ContainerCertificatePathsParameters, _container_certificate_paths).get("default_certificate_bundle_paths")
                default_certificate_dir_paths = cast(ContainerCertificatePathsParameters, _container_certificate_paths).get("default_certificate_dir_paths")
                __builder.write(f'\n    .WithContainerCertificatePaths(customCertificatesDestination: {_format_string(custom_certificates_destination, None)}, defaultCertificateBundlePaths: {_format_value(default_certificate_bundle_paths, None)}, defaultCertificateDirectoryPaths: {_format_value(default_certificate_dir_paths, None)})')
            elif _container_certificate_paths is True:
                __builder.write(f'\n    .WithContainerCertificatePaths()')
            else:
                raise TypeError("Invalid type for option 'container_certificate_paths'")
        if _container_files := kwargs.pop("container_files", None):
            if _validate_tuple_types(_container_files, (str, str)):
                destination_path, source_path, = cast(tuple[str, str], _container_files)
                default_owner = None
                default_group = None
                umask = None
                __builder.write(f'\n    .WithContainerFiles(destinationPath: {_format_string(destination_path, None)}, sourcePath: {_format_string(source_path, None)}, defaultOwner: {_format_value(default_owner, None)}, defaultGroup: {_format_value(default_group, None)}, umask: {_format_value(umask, None)})')
            elif _validate_dict_types(_container_files, ContainerFilesParameters):
                destination_path = cast(ContainerFilesParameters, _container_files)["destination_path"]
                source_path = cast(ContainerFilesParameters, _container_files)["source_path"]
                default_owner = cast(ContainerFilesParameters, _container_files).get("default_owner")
                default_group = cast(ContainerFilesParameters, _container_files).get("default_group")
                umask = cast(ContainerFilesParameters, _container_files).get("umask")
                __builder.write(f'\n    .WithContainerFiles(destinationPath: {_format_string(destination_path, None)}, sourcePath: {_format_string(source_path, None)}, defaultOwner: {_format_value(default_owner, None)}, defaultGroup: {_format_value(default_group, None)}, umask: {_format_value(umask, None)})')
            else:
                raise TypeError("Invalid type for option 'container_files'")
        if _endpoint_proxy_support := kwargs.pop("endpoint_proxy_support", None):
            if _validate_type(_endpoint_proxy_support, bool):
                proxy_enabled = cast(bool, _endpoint_proxy_support)
                __builder.write(f'\n    .WithEndpointProxySupport(proxyEnabled: {_format_bool(proxy_enabled, None)})')
            else:
                raise TypeError("Invalid type for option 'endpoint_proxy_support'")
        if _otlp_exporter := kwargs.pop("otlp_exporter", None):
            if _otlp_exporter is True:
                __builder.write(f'\n    .WithOtlpExporter()')
            elif _validate_type(_otlp_exporter, OtlpProtocol):
                protocol = cast(OtlpProtocol, _otlp_exporter)
                __builder.write(f'\n    .WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)})')
            else:
                raise TypeError("Invalid type for option 'otlp_exporter'")
        if _env := kwargs.pop("env", None):
            if _validate_tuple_types(_env, (str, str)):
                name, value, = cast(tuple[str, str], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)})')
            elif _validate_tuple_types(_env, (str, ExternalServiceResource)):
                name, external_service, = cast(tuple[str, ExternalServiceResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name})')
            elif _validate_tuple_types(_env, (str, ParameterResource)):
                name, parameter, = cast(tuple[str, ParameterResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name})')
            elif _validate_tuple_types(_env, (str, ResourceWithConnectionString)):
                env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], _env)
                __builder.write(f'\n    .WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name})')
            else:
                raise TypeError("Invalid type for option 'env'")
        if _args := kwargs.pop("args", None):
            if _validate_type(_args, Iterable[str]):
                args = cast(Iterable[str], _args)
                __builder.write(f'\n    .WithArgs(args: {_format_string_array(args)})')
            else:
                raise TypeError("Invalid type for option 'args'")
        if _reference_env := kwargs.pop("reference_env", None):
            if _validate_type(_reference_env, ReferenceEnvironmentInjectionFlags):
                flags = cast(ReferenceEnvironmentInjectionFlags, _reference_env)
                __builder.write(f'\n    .WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)})')
            else:
                raise TypeError("Invalid type for option 'reference_env'")
        if _reference := kwargs.pop("reference", None):
            if _validate_type(_reference, ResourceWithConnectionString):
                source = cast(ResourceWithConnectionString, _reference)
                connection_name = None
                optional = None
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_dict_types(_reference, Reference1Parameters):
                source = cast(Reference1Parameters, _reference)["source"]
                connection_name = cast(Reference1Parameters, _reference).get("connection_name")
                optional = cast(Reference1Parameters, _reference).get("optional")
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_type(_reference, ResourceWithServiceDiscovery):
                source = cast(ResourceWithServiceDiscovery, _reference)
                __builder.write(f'\n    .WithReference(source: {source.name})')
            elif _validate_type(_reference, ExternalServiceResource):
                external_service = cast(ExternalServiceResource, _reference)
                __builder.write(f'\n    .WithReference(externalService: {external_service.name})')
            elif _validate_tuple_types(_reference, (ResourceWithServiceDiscovery, str)):
                source, name, = cast(tuple[ResourceWithServiceDiscovery, str], _reference)
                __builder.write(f'\n    .WithReference(source: {source.name}, name: {_format_string(name, None)})')
            else:
                raise TypeError("Invalid type for option 'reference'")
        if _endpoint := kwargs.pop("endpoint", None):
            if _validate_dict_types(_endpoint, EndpointParameters):
                port = cast(EndpointParameters, _endpoint).get("port")
                target_port = cast(EndpointParameters, _endpoint).get("target_port")
                scheme = cast(EndpointParameters, _endpoint).get("scheme")
                name = cast(EndpointParameters, _endpoint).get("name")
                env = cast(EndpointParameters, _endpoint).get("env")
                is_proxied = cast(EndpointParameters, _endpoint).get("is_proxied")
                is_external = cast(EndpointParameters, _endpoint).get("is_external")
                protocol = cast(EndpointParameters, _endpoint).get("protocol")
                __builder.write(f'\n    .WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)})')
            elif _endpoint is True:
                __builder.write(f'\n    .WithEndpoint()')
            else:
                raise TypeError("Invalid type for option 'endpoint'")
        if _http_endpoint := kwargs.pop("http_endpoint", None):
            if _validate_dict_types(_http_endpoint, HttpEndpointParameters):
                port = cast(HttpEndpointParameters, _http_endpoint).get("port")
                target_port = cast(HttpEndpointParameters, _http_endpoint).get("target_port")
                name = cast(HttpEndpointParameters, _http_endpoint).get("name")
                env = cast(HttpEndpointParameters, _http_endpoint).get("env")
                is_proxied = cast(HttpEndpointParameters, _http_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _http_endpoint is True:
                __builder.write(f'\n    .WithHttpEndpoint()')
            else:
                raise TypeError("Invalid type for option 'http_endpoint'")
        if _https_endpoint := kwargs.pop("https_endpoint", None):
            if _validate_dict_types(_https_endpoint, HttpsEndpointParameters):
                port = cast(HttpsEndpointParameters, _https_endpoint).get("port")
                target_port = cast(HttpsEndpointParameters, _https_endpoint).get("target_port")
                name = cast(HttpsEndpointParameters, _https_endpoint).get("name")
                env = cast(HttpsEndpointParameters, _https_endpoint).get("env")
                is_proxied = cast(HttpsEndpointParameters, _https_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _https_endpoint is True:
                __builder.write(f'\n    .WithHttpsEndpoint()')
            else:
                raise TypeError("Invalid type for option 'https_endpoint'")
        if _external_http_endpoints := kwargs.pop("external_http_endpoints", None):
            if _external_http_endpoints is True:
                __builder.write(f'\n    .WithExternalHttpEndpoints()')
            else:
                raise TypeError("Invalid type for option 'external_http_endpoints'")
        if _as_http2_service := kwargs.pop("as_http2_service", None):
            if _as_http2_service is True:
                __builder.write(f'\n    .AsHttp2Service()')
            else:
                raise TypeError("Invalid type for option 'as_http2_service'")
        if _wait_for := kwargs.pop("wait_for", None):
            if _validate_type(_wait_for, Resource):
                dependency = cast(Resource, _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for'")
        if _wait_for_start := kwargs.pop("wait_for_start", None):
            if _validate_type(_wait_for_start, Resource):
                dependency = cast(Resource, _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for_start, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_start'")
        if _wait_for_completion := kwargs.pop("wait_for_completion", None):
            if _validate_type(_wait_for_completion, Resource):
                dependency = cast(Resource, _wait_for_completion)
                exit_code = None
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            elif _validate_tuple_types(_wait_for_completion, (Resource, int)):
                dependency, exit_code = cast(tuple[Resource, int], _wait_for_completion)
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_completion'")
        if _http_health_check := kwargs.pop("http_health_check", None):
            if _validate_dict_types(_http_health_check, HttpHealthCheckParameters):
                path = cast(HttpHealthCheckParameters, _http_health_check).get("path")
                status_code = cast(HttpHealthCheckParameters, _http_health_check).get("status_code")
                endpoint_name = cast(HttpHealthCheckParameters, _http_health_check).get("endpoint_name")
                __builder.write(f'\n    .WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _http_health_check is True:
                __builder.write(f'\n    .WithHttpHealthCheck()')
            else:
                raise TypeError("Invalid type for option 'http_health_check'")
        if _http_command := kwargs.pop("http_command", None):
            if _validate_tuple_types(_http_command, (str, str)):
                path, display_name, = cast(tuple[str, str], _http_command)
                endpoint_name = None
                command_name = None
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            elif _validate_dict_types(_http_command, HttpCommandParameters):
                path = cast(HttpCommandParameters, _http_command)["path"]
                display_name = cast(HttpCommandParameters, _http_command)["display_name"]
                endpoint_name = cast(HttpCommandParameters, _http_command).get("endpoint_name")
                command_name = cast(HttpCommandParameters, _http_command).get("command_name")
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_command'")
        if _certificate_authority_collection := kwargs.pop("certificate_authority_collection", None):
            if _validate_type(_certificate_authority_collection, CertificateAuthorityCollection):
                certificate_authority_collection = cast(CertificateAuthorityCollection, _certificate_authority_collection)
                __builder.write(f'\n    .WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name})')
            else:
                raise TypeError("Invalid type for option 'certificate_authority_collection'")
        if _developer_certificate_trust := kwargs.pop("developer_certificate_trust", None):
            if _validate_type(_developer_certificate_trust, bool):
                trust = cast(bool, _developer_certificate_trust)
                __builder.write(f'\n    .WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)})')
            else:
                raise TypeError("Invalid type for option 'developer_certificate_trust'")
        if _certificate_trust_scope := kwargs.pop("certificate_trust_scope", None):
            if _validate_type(_certificate_trust_scope, CertificateTrustScope):
                scope = cast(CertificateTrustScope, _certificate_trust_scope)
                __builder.write(f'\n    .WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)})')
            else:
                raise TypeError("Invalid type for option 'certificate_trust_scope'")
        if _compute_env := kwargs.pop("compute_env", None):
            if _validate_type(_compute_env, ComputeEnvironmentResource):
                compute_env_resource = cast(ComputeEnvironmentResource, _compute_env)
                __builder.write(f'\n    .WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name})')
            else:
                raise TypeError("Invalid type for option 'compute_env'")
        if _http_probe := kwargs.pop("http_probe", None):
            if _validate_type(_http_probe, ProbeType):
                type = cast(ProbeType, _http_probe)
                path = None
                initial_delay_seconds = None
                period_seconds = None
                timeout_seconds = None
                failure_threshold = None
                success_threshold = None
                endpoint_name = None
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _validate_dict_types(_http_probe, HttpProbeParameters):
                type = cast(HttpProbeParameters, _http_probe)["type"]
                path = cast(HttpProbeParameters, _http_probe).get("path")
                initial_delay_seconds = cast(HttpProbeParameters, _http_probe).get("initial_delay_seconds")
                period_seconds = cast(HttpProbeParameters, _http_probe).get("period_seconds")
                timeout_seconds = cast(HttpProbeParameters, _http_probe).get("timeout_seconds")
                failure_threshold = cast(HttpProbeParameters, _http_probe).get("failure_threshold")
                success_threshold = cast(HttpProbeParameters, _http_probe).get("success_threshold")
                endpoint_name = cast(HttpProbeParameters, _http_probe).get("endpoint_name")
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_probe'")
        super().__init__(__name, __builder, **kwargs)

    @overload
    def with_volume(self, target: str, /) -> Self:
        ...
    @overload
    def with_volume(self, name: str | None, target: str, /, *, is_read_only: bool = False) -> Self:
        ...
    def with_volume(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], str):
            target = cast(str, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with target")
            self._builder.write(f'\n{self.name}.WithVolume(target: {_format_string(target, None)});')
            return self
        elif _validate_tuple_types(args + (_is_read_only := kwargs.get("is_read_only", False),), (str | None, str, bool | Literal[False])):
            name, target, = cast(tuple[str, str], args)
            is_read_only = _is_read_only
            self._builder.write(f'\n{self.name}.WithVolume(name: {_format_string(name, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_bind_mount(self, source: str, target: str, /, *, is_read_only: bool = False) -> Self:
        if _validate_tuple_types((source, target, is_read_only), (str, str, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithBindMount(source: {_format_string(source, None)}, target: {_format_string(target, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_entrypoint(self, entrypoint: str, /) -> Self:
        if _validate_type(entrypoint, str):
            self._builder.write(f'\n{self.name}.WithEntrypoint(entrypoint: {_format_string(entrypoint, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_image_tag(self, tag: str, /) -> Self:
        if _validate_type(tag, str):
            self._builder.write(f'\n{self.name}.WithImageTag(tag: {_format_string(tag, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_image_registry(self, registry: str | None, /) -> Self:
        if _validate_type(registry, str | None):
            self._builder.write(f'\n{self.name}.WithImageRegistry(registry: {_format_string(registry, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_image(self, image: str, /, *, tag: str | None = None) -> Self:
        if _validate_tuple_types((image, tag), (str, str | None)):
            self._builder.write(f'\n{self.name}.WithImage(image: {_format_string(image, None)}, tag: {_format_string(tag, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_image_sha256(self, sha256: str, /) -> Self:
        if _validate_type(sha256, str):
            self._builder.write(f'\n{self.name}.WithImageSHA256(sha256: {_format_string(sha256, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_container_runtime_args(self, args: Iterable[str], /) -> Self:
        if _validate_type(args, Iterable[str]):
            self._builder.write(f'\n{self.name}.WithContainerRuntimeArgs(args: {_format_string_array(args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_lifetime(self, lifetime: ContainerLifetime, /) -> Self:
        if _validate_type(lifetime, ContainerLifetime):
            self._builder.write(f'\n{self.name}.WithLifetime(lifetime: {_format_enum("ContainerLifetime", lifetime, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_image_pull_policy(self, pull_policy: ImagePullPolicy, /) -> Self:
        if _validate_type(pull_policy, ImagePullPolicy):
            self._builder.write(f'\n{self.name}.WithImagePullPolicy(pullPolicy: {_format_enum("ImagePullPolicy", pull_policy, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def publish_as_container(self) -> Self:
        self._builder.write(f'\n{self.name}.PublishAsContainer();')
        return self

    def with_dockerfile(self, context_path: str, /, *, dockerfile_path: str | None = None, stage: str | None = None) -> Self:
        if _validate_tuple_types((context_path, dockerfile_path, stage), (str, str | None, str | None)):
            self._builder.write(f'\n{self.name}.WithDockerfile(contextPath: {_format_string(context_path, None)}, dockerfilePath: {_format_string(dockerfile_path, None)}, stage: {_format_string(stage, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_container_name(self, name: str, /) -> Self:
        if _validate_type(name, str):
            self._builder.write(f'\n{self.name}.WithContainerName(name: {_format_string(name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_build_arg(self, name: str, value: ParameterResource, /) -> Self:
        if _validate_tuple_types((name, value, ), (str, ParameterResource)):
            self._builder.write(f'\n{self.name}.WithBuildArg(name: {_format_string(name, None)}, value: {value.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_build_secret(self, name: str, value: ParameterResource, /) -> Self:
        if _validate_tuple_types((name, value, ), (str, ParameterResource)):
            self._builder.write(f'\n{self.name}.WithBuildSecret(name: {_format_string(name, None)}, value: {value.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_container_certificate_paths(self, *, custom_certificates_destination: str | None = None, default_certificate_bundle_paths: Iterable[str] | None = None, default_certificate_dir_paths: Iterable[str] | None = None) -> Self:
        if _validate_tuple_types((custom_certificates_destination, default_certificate_bundle_paths, default_certificate_dir_paths), (str | None, Iterable[str] | None, Iterable[str] | None)):
            self._builder.write(f'\n{self.name}.WithContainerCertificatePaths(customCertificatesDestination: {_format_string(custom_certificates_destination, None)}, defaultCertificateBundlePaths: {_format_value(default_certificate_bundle_paths, None)}, defaultCertificateDirectoryPaths: {_format_value(default_certificate_dir_paths, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_container_files(self, destination_path: str, source_path: str, /, *, default_owner: int | None = None, default_group: int | None = None, umask: UnixFileMode | None = None) -> Self:
        if _validate_tuple_types((destination_path, source_path, default_owner, default_group, umask), (str, str, int | None, int | None, UnixFileMode | None)):
            self._builder.write(f'\n{self.name}.WithContainerFiles(destinationPath: {_format_string(destination_path, None)}, sourcePath: {_format_string(source_path, None)}, defaultOwner: {_format_value(default_owner, None)}, defaultGroup: {_format_value(default_group, None)}, umask: {_format_value(umask, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_endpoint_proxy_support(self, proxy_enabled: bool, /) -> Self:
        if _validate_type(proxy_enabled, bool):
            with _experimental(self._builder, "with_endpoint_proxy_support", self.__class__, "ASPIREPROXYENDPOINTS001"):
                self._builder.write(f'\n{self.name}.WithEndpointProxySupport(proxyEnabled: {_format_bool(proxy_enabled, None)});')
                return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_otlp_exporter(self) -> Self:
        ...
    @overload
    def with_otlp_exporter(self, protocol: OtlpProtocol, /) -> Self:
        ...
    def with_otlp_exporter(self, *args, **kwargs) -> Self:
        if not args and not kwargs:
            self._builder.write(f'\n{self.name}.WithOtlpExporter();')
            return self
        elif len(args) == 1 and _validate_type(args[0], OtlpProtocol):
            protocol = cast(OtlpProtocol, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with protocol")
            self._builder.write(f'\n{self.name}.WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_env(self, name: str, value: str | None, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, parameter: ParameterResource, /) -> Self:
        ...
    @overload
    def with_env(self, env_var_name: str, resource: ResourceWithConnectionString, /) -> Self:
        ...
    def with_env(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (), (str, str | None)):
            name, value, = cast(tuple[str, str], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)});')
            return self
        elif _validate_tuple_types(args + (), (str, ExternalServiceResource)):
            name, external_service, = cast(tuple[str, ExternalServiceResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ParameterResource)):
            name, parameter, = cast(tuple[str, ParameterResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ResourceWithConnectionString)):
            env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_args(self, args: Iterable[str], /) -> Self:
        if _validate_type(args, Iterable[str]):
            self._builder.write(f'\n{self.name}.WithArgs(args: {_format_string_array(args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_reference_env(self, flags: ReferenceEnvironmentInjectionFlags, /) -> Self:
        if _validate_type(flags, ReferenceEnvironmentInjectionFlags):
            self._builder.write(f'\n{self.name}.WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_reference(self, source: ResourceWithConnectionString, /, *, connection_name: str | None = None, optional: bool = False) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, /) -> Self:
        ...
    @overload
    def with_reference(self, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, name: str, /) -> Self:
        ...
    def with_reference(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (_connection_name := kwargs.get("connection_name", None), _optional := kwargs.get("optional", False),), (ResourceWithConnectionString, str | None, bool | Literal[False])):
            source, = cast(tuple[ResourceWithConnectionString], args)
            connection_name = _connection_name
            optional = _optional
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ResourceWithServiceDiscovery):
            source = cast(ResourceWithServiceDiscovery, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with source")
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ExternalServiceResource):
            external_service = cast(ExternalServiceResource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with external_service")
            self._builder.write(f'\n{self.name}.WithReference(externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (ResourceWithServiceDiscovery, str)):
            source, name, = cast(tuple[ResourceWithServiceDiscovery, str], args)
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, name: {_format_string(name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_endpoint(self, *, port: int | None = None, target_port: int | None = None, scheme: str | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True, is_external: bool | None = None, protocol: ProtocolType | None = None) -> Self:
        if _validate_tuple_types((port, target_port, scheme, name, env, is_proxied, is_external, protocol), (int | None, int | None, str | None, str | None, str | None, bool | Literal[True], bool | None, ProtocolType | None)):
            self._builder.write(f'\n{self.name}.WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_https_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_external_http_endpoints(self) -> Self:
        self._builder.write(f'\n{self.name}.WithExternalHttpEndpoints();')
        return self

    def as_http2_service(self) -> Self:
        self._builder.write(f'\n{self.name}.AsHttp2Service();')
        return self

    @overload
    def wait_for(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for_start(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for_start(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for_start(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def wait_for_completion(self, dependency: Resource, /, *, exit_code: int = 0) -> Self:
        if _validate_tuple_types((dependency, exit_code), (Resource, int | Literal[0])):
            self._builder.write(f'\n{self.name}.WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_health_check(self, *, path: str | None = None, status_code: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((path, status_code, endpoint_name), (str | None, int | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_command(self, path: str, display_name: str, /, *, endpoint_name: str | None = None, command_name: str | None = None) -> Self:
        if _validate_tuple_types((path, display_name, endpoint_name, command_name), (str, str, str | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_authority_collection(self, certificate_authority_collection: CertificateAuthorityCollection, /) -> Self:
        if _validate_type(certificate_authority_collection, CertificateAuthorityCollection):
            self._builder.write(f'\n{self.name}.WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_developer_certificate_trust(self, trust: bool, /) -> Self:
        if _validate_type(trust, bool):
            self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_trust_scope(self, scope: CertificateTrustScope, /) -> Self:
        if _validate_type(scope, CertificateTrustScope):
            self._builder.write(f'\n{self.name}.WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_compute_env(self, compute_env_resource: ComputeEnvironmentResource, /) -> Self:
        if _validate_type(compute_env_resource, ComputeEnvironmentResource):
            self._builder.write(f'\n{self.name}.WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_probe(self, type: ProbeType, /, *, path: str | None = None, initial_delay_seconds: int | None = None, period_seconds: int | None = None, timeout_seconds: int | None = None, failure_threshold: int | None = None, success_threshold: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((type, path, initial_delay_seconds, period_seconds, timeout_seconds, failure_threshold, success_threshold, endpoint_name), (ProbeType, str | None, int | None, int | None, int | None, int | None, int | None, str | None)):
            with _experimental(self._builder, "with_http_probe", self.__class__, "ASPIREPROBES001"):
                self._builder.write(f'\n{self.name}.WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)});')
                return self
        else:
            raise TypeError("No matching overload found.")


class ProjectResourceOptions(_BaseResourceOptions, total=False):
    """Options for ProjectResource"""
    replicas: int
    disable_forwarded_headers: Literal[True]
    otlp_exporter: Literal[True] | OtlpProtocol
    publish_as_docker_file: Literal[True]
    env: tuple[str, str] | tuple[str, ExternalServiceResource] | tuple[str, ParameterResource] | tuple[str, ResourceWithConnectionString]
    args: Iterable[str]
    reference_env: ReferenceEnvironmentInjectionFlags
    reference: ResourceWithConnectionString | Reference1Parameters | ResourceWithServiceDiscovery | ExternalServiceResource | tuple[ResourceWithServiceDiscovery, str]
    endpoint: EndpointParameters | Literal[True]
    http_endpoint: HttpEndpointParameters | Literal[True]
    https_endpoint: HttpsEndpointParameters | Literal[True]
    external_http_endpoints: Literal[True]
    as_http2_service: Literal[True]
    publish_with_container_files: tuple[ResourceWithContainerFiles, str]
    wait_for: Resource | tuple[Resource, WaitBehavior]
    wait_for_start: Resource | tuple[Resource, WaitBehavior]
    wait_for_completion: Resource | tuple[Resource, int]
    http_health_check: HttpHealthCheckParameters | Literal[True]
    http_command: tuple[str, str] | HttpCommandParameters
    certificate_authority_collection: CertificateAuthorityCollection
    developer_certificate_trust: bool
    certificate_trust_scope: CertificateTrustScope
    compute_env: ComputeEnvironmentResource
    http_probe: Annotated[ProbeType | HttpProbeParameters, Warnings(experimental="ASPIREPROBES001")]


class ProjectResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ProjectResourceOptions]) -> None:
        if _replicas := kwargs.pop("replicas", None):
            if _validate_type(_replicas, int):
                replicas = cast(int, _replicas)
                __builder.write(f'\n    .WithReplicas(replicas: {_format_value(replicas, None)})')
            else:
                raise TypeError("Invalid type for option 'replicas'")
        if _disable_forwarded_headers := kwargs.pop("disable_forwarded_headers", None):
            if _disable_forwarded_headers is True:
                __builder.write(f'\n    .DisableForwardedHeaders()')
            else:
                raise TypeError("Invalid type for option 'disable_forwarded_headers'")
        if _otlp_exporter := kwargs.pop("otlp_exporter", None):
            if _otlp_exporter is True:
                __builder.write(f'\n    .WithOtlpExporter()')
            elif _validate_type(_otlp_exporter, OtlpProtocol):
                protocol = cast(OtlpProtocol, _otlp_exporter)
                __builder.write(f'\n    .WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)})')
            else:
                raise TypeError("Invalid type for option 'otlp_exporter'")
        if _publish_as_docker_file := kwargs.pop("publish_as_docker_file", None):
            if _publish_as_docker_file is True:
                __builder.write(f'\n    .PublishAsDockerFile()')
            else:
                raise TypeError("Invalid type for option 'publish_as_docker_file'")
        if _env := kwargs.pop("env", None):
            if _validate_tuple_types(_env, (str, str)):
                name, value, = cast(tuple[str, str], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)})')
            elif _validate_tuple_types(_env, (str, ExternalServiceResource)):
                name, external_service, = cast(tuple[str, ExternalServiceResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name})')
            elif _validate_tuple_types(_env, (str, ParameterResource)):
                name, parameter, = cast(tuple[str, ParameterResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name})')
            elif _validate_tuple_types(_env, (str, ResourceWithConnectionString)):
                env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], _env)
                __builder.write(f'\n    .WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name})')
            else:
                raise TypeError("Invalid type for option 'env'")
        if _args := kwargs.pop("args", None):
            if _validate_type(_args, Iterable[str]):
                args = cast(Iterable[str], _args)
                __builder.write(f'\n    .WithArgs(args: {_format_string_array(args)})')
            else:
                raise TypeError("Invalid type for option 'args'")
        if _reference_env := kwargs.pop("reference_env", None):
            if _validate_type(_reference_env, ReferenceEnvironmentInjectionFlags):
                flags = cast(ReferenceEnvironmentInjectionFlags, _reference_env)
                __builder.write(f'\n    .WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)})')
            else:
                raise TypeError("Invalid type for option 'reference_env'")
        if _reference := kwargs.pop("reference", None):
            if _validate_type(_reference, ResourceWithConnectionString):
                source = cast(ResourceWithConnectionString, _reference)
                connection_name = None
                optional = None
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_dict_types(_reference, Reference1Parameters):
                source = cast(Reference1Parameters, _reference)["source"]
                connection_name = cast(Reference1Parameters, _reference).get("connection_name")
                optional = cast(Reference1Parameters, _reference).get("optional")
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_type(_reference, ResourceWithServiceDiscovery):
                source = cast(ResourceWithServiceDiscovery, _reference)
                __builder.write(f'\n    .WithReference(source: {source.name})')
            elif _validate_type(_reference, ExternalServiceResource):
                external_service = cast(ExternalServiceResource, _reference)
                __builder.write(f'\n    .WithReference(externalService: {external_service.name})')
            elif _validate_tuple_types(_reference, (ResourceWithServiceDiscovery, str)):
                source, name, = cast(tuple[ResourceWithServiceDiscovery, str], _reference)
                __builder.write(f'\n    .WithReference(source: {source.name}, name: {_format_string(name, None)})')
            else:
                raise TypeError("Invalid type for option 'reference'")
        if _endpoint := kwargs.pop("endpoint", None):
            if _validate_dict_types(_endpoint, EndpointParameters):
                port = cast(EndpointParameters, _endpoint).get("port")
                target_port = cast(EndpointParameters, _endpoint).get("target_port")
                scheme = cast(EndpointParameters, _endpoint).get("scheme")
                name = cast(EndpointParameters, _endpoint).get("name")
                env = cast(EndpointParameters, _endpoint).get("env")
                is_proxied = cast(EndpointParameters, _endpoint).get("is_proxied")
                is_external = cast(EndpointParameters, _endpoint).get("is_external")
                protocol = cast(EndpointParameters, _endpoint).get("protocol")
                __builder.write(f'\n    .WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)})')
            elif _endpoint is True:
                __builder.write(f'\n    .WithEndpoint()')
            else:
                raise TypeError("Invalid type for option 'endpoint'")
        if _http_endpoint := kwargs.pop("http_endpoint", None):
            if _validate_dict_types(_http_endpoint, HttpEndpointParameters):
                port = cast(HttpEndpointParameters, _http_endpoint).get("port")
                target_port = cast(HttpEndpointParameters, _http_endpoint).get("target_port")
                name = cast(HttpEndpointParameters, _http_endpoint).get("name")
                env = cast(HttpEndpointParameters, _http_endpoint).get("env")
                is_proxied = cast(HttpEndpointParameters, _http_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _http_endpoint is True:
                __builder.write(f'\n    .WithHttpEndpoint()')
            else:
                raise TypeError("Invalid type for option 'http_endpoint'")
        if _https_endpoint := kwargs.pop("https_endpoint", None):
            if _validate_dict_types(_https_endpoint, HttpsEndpointParameters):
                port = cast(HttpsEndpointParameters, _https_endpoint).get("port")
                target_port = cast(HttpsEndpointParameters, _https_endpoint).get("target_port")
                name = cast(HttpsEndpointParameters, _https_endpoint).get("name")
                env = cast(HttpsEndpointParameters, _https_endpoint).get("env")
                is_proxied = cast(HttpsEndpointParameters, _https_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _https_endpoint is True:
                __builder.write(f'\n    .WithHttpsEndpoint()')
            else:
                raise TypeError("Invalid type for option 'https_endpoint'")
        if _external_http_endpoints := kwargs.pop("external_http_endpoints", None):
            if _external_http_endpoints is True:
                __builder.write(f'\n    .WithExternalHttpEndpoints()')
            else:
                raise TypeError("Invalid type for option 'external_http_endpoints'")
        if _as_http2_service := kwargs.pop("as_http2_service", None):
            if _as_http2_service is True:
                __builder.write(f'\n    .AsHttp2Service()')
            else:
                raise TypeError("Invalid type for option 'as_http2_service'")
        if _publish_with_container_files := kwargs.pop("publish_with_container_files", None):
            if _validate_tuple_types(_publish_with_container_files, (ResourceWithContainerFiles, str)):
                source, destination_path, = cast(tuple[ResourceWithContainerFiles, str], _publish_with_container_files)
                __builder.write(f'\n    .PublishWithContainerFiles(source: {source.name}, destinationPath: {_format_string(destination_path, None)})')
            else:
                raise TypeError("Invalid type for option 'publish_with_container_files'")
        if _wait_for := kwargs.pop("wait_for", None):
            if _validate_type(_wait_for, Resource):
                dependency = cast(Resource, _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for'")
        if _wait_for_start := kwargs.pop("wait_for_start", None):
            if _validate_type(_wait_for_start, Resource):
                dependency = cast(Resource, _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for_start, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_start'")
        if _wait_for_completion := kwargs.pop("wait_for_completion", None):
            if _validate_type(_wait_for_completion, Resource):
                dependency = cast(Resource, _wait_for_completion)
                exit_code = None
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            elif _validate_tuple_types(_wait_for_completion, (Resource, int)):
                dependency, exit_code = cast(tuple[Resource, int], _wait_for_completion)
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_completion'")
        if _http_health_check := kwargs.pop("http_health_check", None):
            if _validate_dict_types(_http_health_check, HttpHealthCheckParameters):
                path = cast(HttpHealthCheckParameters, _http_health_check).get("path")
                status_code = cast(HttpHealthCheckParameters, _http_health_check).get("status_code")
                endpoint_name = cast(HttpHealthCheckParameters, _http_health_check).get("endpoint_name")
                __builder.write(f'\n    .WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _http_health_check is True:
                __builder.write(f'\n    .WithHttpHealthCheck()')
            else:
                raise TypeError("Invalid type for option 'http_health_check'")
        if _http_command := kwargs.pop("http_command", None):
            if _validate_tuple_types(_http_command, (str, str)):
                path, display_name, = cast(tuple[str, str], _http_command)
                endpoint_name = None
                command_name = None
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            elif _validate_dict_types(_http_command, HttpCommandParameters):
                path = cast(HttpCommandParameters, _http_command)["path"]
                display_name = cast(HttpCommandParameters, _http_command)["display_name"]
                endpoint_name = cast(HttpCommandParameters, _http_command).get("endpoint_name")
                command_name = cast(HttpCommandParameters, _http_command).get("command_name")
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_command'")
        if _certificate_authority_collection := kwargs.pop("certificate_authority_collection", None):
            if _validate_type(_certificate_authority_collection, CertificateAuthorityCollection):
                certificate_authority_collection = cast(CertificateAuthorityCollection, _certificate_authority_collection)
                __builder.write(f'\n    .WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name})')
            else:
                raise TypeError("Invalid type for option 'certificate_authority_collection'")
        if _developer_certificate_trust := kwargs.pop("developer_certificate_trust", None):
            if _validate_type(_developer_certificate_trust, bool):
                trust = cast(bool, _developer_certificate_trust)
                __builder.write(f'\n    .WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)})')
            else:
                raise TypeError("Invalid type for option 'developer_certificate_trust'")
        if _certificate_trust_scope := kwargs.pop("certificate_trust_scope", None):
            if _validate_type(_certificate_trust_scope, CertificateTrustScope):
                scope = cast(CertificateTrustScope, _certificate_trust_scope)
                __builder.write(f'\n    .WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)})')
            else:
                raise TypeError("Invalid type for option 'certificate_trust_scope'")
        if _compute_env := kwargs.pop("compute_env", None):
            if _validate_type(_compute_env, ComputeEnvironmentResource):
                compute_env_resource = cast(ComputeEnvironmentResource, _compute_env)
                __builder.write(f'\n    .WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name})')
            else:
                raise TypeError("Invalid type for option 'compute_env'")
        if _http_probe := kwargs.pop("http_probe", None):
            if _validate_type(_http_probe, ProbeType):
                type = cast(ProbeType, _http_probe)
                path = None
                initial_delay_seconds = None
                period_seconds = None
                timeout_seconds = None
                failure_threshold = None
                success_threshold = None
                endpoint_name = None
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _validate_dict_types(_http_probe, HttpProbeParameters):
                type = cast(HttpProbeParameters, _http_probe)["type"]
                path = cast(HttpProbeParameters, _http_probe).get("path")
                initial_delay_seconds = cast(HttpProbeParameters, _http_probe).get("initial_delay_seconds")
                period_seconds = cast(HttpProbeParameters, _http_probe).get("period_seconds")
                timeout_seconds = cast(HttpProbeParameters, _http_probe).get("timeout_seconds")
                failure_threshold = cast(HttpProbeParameters, _http_probe).get("failure_threshold")
                success_threshold = cast(HttpProbeParameters, _http_probe).get("success_threshold")
                endpoint_name = cast(HttpProbeParameters, _http_probe).get("endpoint_name")
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_probe'")
        super().__init__(__name, __builder, **kwargs)

    def with_replicas(self, replicas: int, /) -> Self:
        if _validate_type(replicas, int):
            self._builder.write(f'\n{self.name}.WithReplicas(replicas: {_format_value(replicas, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def disable_forwarded_headers(self) -> Self:
        self._builder.write(f'\n{self.name}.DisableForwardedHeaders();')
        return self

    @overload
    def with_otlp_exporter(self) -> Self:
        ...
    @overload
    def with_otlp_exporter(self, protocol: OtlpProtocol, /) -> Self:
        ...
    def with_otlp_exporter(self, *args, **kwargs) -> Self:
        if not args and not kwargs:
            self._builder.write(f'\n{self.name}.WithOtlpExporter();')
            return self
        elif len(args) == 1 and _validate_type(args[0], OtlpProtocol):
            protocol = cast(OtlpProtocol, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with protocol")
            self._builder.write(f'\n{self.name}.WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def publish_as_docker_file(self) -> Self:
        self._builder.write(f'\n{self.name}.PublishAsDockerFile();')
        return self

    @overload
    def with_env(self, name: str, value: str | None, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, parameter: ParameterResource, /) -> Self:
        ...
    @overload
    def with_env(self, env_var_name: str, resource: ResourceWithConnectionString, /) -> Self:
        ...
    def with_env(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (), (str, str | None)):
            name, value, = cast(tuple[str, str], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)});')
            return self
        elif _validate_tuple_types(args + (), (str, ExternalServiceResource)):
            name, external_service, = cast(tuple[str, ExternalServiceResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ParameterResource)):
            name, parameter, = cast(tuple[str, ParameterResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ResourceWithConnectionString)):
            env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_args(self, args: Iterable[str], /) -> Self:
        if _validate_type(args, Iterable[str]):
            self._builder.write(f'\n{self.name}.WithArgs(args: {_format_string_array(args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_reference_env(self, flags: ReferenceEnvironmentInjectionFlags, /) -> Self:
        if _validate_type(flags, ReferenceEnvironmentInjectionFlags):
            self._builder.write(f'\n{self.name}.WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_reference(self, source: ResourceWithConnectionString, /, *, connection_name: str | None = None, optional: bool = False) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, /) -> Self:
        ...
    @overload
    def with_reference(self, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, name: str, /) -> Self:
        ...
    def with_reference(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (_connection_name := kwargs.get("connection_name", None), _optional := kwargs.get("optional", False),), (ResourceWithConnectionString, str | None, bool | Literal[False])):
            source, = cast(tuple[ResourceWithConnectionString], args)
            connection_name = _connection_name
            optional = _optional
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ResourceWithServiceDiscovery):
            source = cast(ResourceWithServiceDiscovery, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with source")
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ExternalServiceResource):
            external_service = cast(ExternalServiceResource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with external_service")
            self._builder.write(f'\n{self.name}.WithReference(externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (ResourceWithServiceDiscovery, str)):
            source, name, = cast(tuple[ResourceWithServiceDiscovery, str], args)
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, name: {_format_string(name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_endpoint(self, *, port: int | None = None, target_port: int | None = None, scheme: str | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True, is_external: bool | None = None, protocol: ProtocolType | None = None) -> Self:
        if _validate_tuple_types((port, target_port, scheme, name, env, is_proxied, is_external, protocol), (int | None, int | None, str | None, str | None, str | None, bool | Literal[True], bool | None, ProtocolType | None)):
            self._builder.write(f'\n{self.name}.WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_https_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_external_http_endpoints(self) -> Self:
        self._builder.write(f'\n{self.name}.WithExternalHttpEndpoints();')
        return self

    def as_http2_service(self) -> Self:
        self._builder.write(f'\n{self.name}.AsHttp2Service();')
        return self

    def publish_with_container_files(self, source: ResourceWithContainerFiles, destination_path: str, /) -> Self:
        if _validate_tuple_types((source, destination_path, ), (ResourceWithContainerFiles, str)):
            self._builder.write(f'\n{self.name}.PublishWithContainerFiles(source: {source.name}, destinationPath: {_format_string(destination_path, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for_start(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for_start(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for_start(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def wait_for_completion(self, dependency: Resource, /, *, exit_code: int = 0) -> Self:
        if _validate_tuple_types((dependency, exit_code), (Resource, int | Literal[0])):
            self._builder.write(f'\n{self.name}.WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_health_check(self, *, path: str | None = None, status_code: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((path, status_code, endpoint_name), (str | None, int | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_command(self, path: str, display_name: str, /, *, endpoint_name: str | None = None, command_name: str | None = None) -> Self:
        if _validate_tuple_types((path, display_name, endpoint_name, command_name), (str, str, str | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_authority_collection(self, certificate_authority_collection: CertificateAuthorityCollection, /) -> Self:
        if _validate_type(certificate_authority_collection, CertificateAuthorityCollection):
            self._builder.write(f'\n{self.name}.WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_developer_certificate_trust(self, trust: bool, /) -> Self:
        if _validate_type(trust, bool):
            self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_trust_scope(self, scope: CertificateTrustScope, /) -> Self:
        if _validate_type(scope, CertificateTrustScope):
            self._builder.write(f'\n{self.name}.WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_compute_env(self, compute_env_resource: ComputeEnvironmentResource, /) -> Self:
        if _validate_type(compute_env_resource, ComputeEnvironmentResource):
            self._builder.write(f'\n{self.name}.WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_probe(self, type: ProbeType, /, *, path: str | None = None, initial_delay_seconds: int | None = None, period_seconds: int | None = None, timeout_seconds: int | None = None, failure_threshold: int | None = None, success_threshold: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((type, path, initial_delay_seconds, period_seconds, timeout_seconds, failure_threshold, success_threshold, endpoint_name), (ProbeType, str | None, int | None, int | None, int | None, int | None, int | None, str | None)):
            with _experimental(self._builder, "with_http_probe", self.__class__, "ASPIREPROBES001"):
                self._builder.write(f'\n{self.name}.WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)});')
                return self
        else:
            raise TypeError("No matching overload found.")


class CSharpAppResourceOptions(ProjectResourceOptions, total=False):
    """Options for CSharpAppResource"""


class CSharpAppResource(ProjectResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[CSharpAppResourceOptions]) -> None:
        super().__init__(__name, __builder, **kwargs)


class ExecutableResourceOptions(_BaseResourceOptions, total=False):
    """Options for ExecutableResource"""
    publish_as_docker_file: Literal[True]
    command: str
    working_dir: str
    otlp_exporter: Literal[True] | OtlpProtocol
    env: tuple[str, str] | tuple[str, ExternalServiceResource] | tuple[str, ParameterResource] | tuple[str, ResourceWithConnectionString]
    args: Iterable[str]
    reference_env: ReferenceEnvironmentInjectionFlags
    reference: ResourceWithConnectionString | Reference1Parameters | ResourceWithServiceDiscovery | ExternalServiceResource | tuple[ResourceWithServiceDiscovery, str]
    endpoint: EndpointParameters | Literal[True]
    http_endpoint: HttpEndpointParameters | Literal[True]
    https_endpoint: HttpsEndpointParameters | Literal[True]
    external_http_endpoints: Literal[True]
    as_http2_service: Literal[True]
    wait_for: Resource | tuple[Resource, WaitBehavior]
    wait_for_start: Resource | tuple[Resource, WaitBehavior]
    wait_for_completion: Resource | tuple[Resource, int]
    http_health_check: HttpHealthCheckParameters | Literal[True]
    http_command: tuple[str, str] | HttpCommandParameters
    certificate_authority_collection: CertificateAuthorityCollection
    developer_certificate_trust: bool
    certificate_trust_scope: CertificateTrustScope
    compute_env: ComputeEnvironmentResource
    http_probe: Annotated[ProbeType | HttpProbeParameters, Warnings(experimental="ASPIREPROBES001")]


class ExecutableResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ExecutableResourceOptions]) -> None:
        if _publish_as_docker_file := kwargs.pop("publish_as_docker_file", None):
            if _publish_as_docker_file is True:
                __builder.write(f'\n    .PublishAsDockerFile()')
            else:
                raise TypeError("Invalid type for option 'publish_as_docker_file'")
        if _command := kwargs.pop("command", None):
            if _validate_type(_command, str):
                command = cast(str, _command)
                __builder.write(f'\n    .WithCommand(command: {_format_string(command, None)})')
            else:
                raise TypeError("Invalid type for option 'command'")
        if _working_dir := kwargs.pop("working_dir", None):
            if _validate_type(_working_dir, str):
                working_dir = cast(str, _working_dir)
                __builder.write(f'\n    .WithWorkingDirectory(workingDirectory: {_format_string(working_dir, None)})')
            else:
                raise TypeError("Invalid type for option 'working_dir'")
        if _otlp_exporter := kwargs.pop("otlp_exporter", None):
            if _otlp_exporter is True:
                __builder.write(f'\n    .WithOtlpExporter()')
            elif _validate_type(_otlp_exporter, OtlpProtocol):
                protocol = cast(OtlpProtocol, _otlp_exporter)
                __builder.write(f'\n    .WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)})')
            else:
                raise TypeError("Invalid type for option 'otlp_exporter'")
        if _env := kwargs.pop("env", None):
            if _validate_tuple_types(_env, (str, str)):
                name, value, = cast(tuple[str, str], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)})')
            elif _validate_tuple_types(_env, (str, ExternalServiceResource)):
                name, external_service, = cast(tuple[str, ExternalServiceResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name})')
            elif _validate_tuple_types(_env, (str, ParameterResource)):
                name, parameter, = cast(tuple[str, ParameterResource], _env)
                __builder.write(f'\n    .WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name})')
            elif _validate_tuple_types(_env, (str, ResourceWithConnectionString)):
                env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], _env)
                __builder.write(f'\n    .WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name})')
            else:
                raise TypeError("Invalid type for option 'env'")
        if _args := kwargs.pop("args", None):
            if _validate_type(_args, Iterable[str]):
                args = cast(Iterable[str], _args)
                __builder.write(f'\n    .WithArgs(args: {_format_string_array(args)})')
            else:
                raise TypeError("Invalid type for option 'args'")
        if _reference_env := kwargs.pop("reference_env", None):
            if _validate_type(_reference_env, ReferenceEnvironmentInjectionFlags):
                flags = cast(ReferenceEnvironmentInjectionFlags, _reference_env)
                __builder.write(f'\n    .WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)})')
            else:
                raise TypeError("Invalid type for option 'reference_env'")
        if _reference := kwargs.pop("reference", None):
            if _validate_type(_reference, ResourceWithConnectionString):
                source = cast(ResourceWithConnectionString, _reference)
                connection_name = None
                optional = None
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_dict_types(_reference, Reference1Parameters):
                source = cast(Reference1Parameters, _reference)["source"]
                connection_name = cast(Reference1Parameters, _reference).get("connection_name")
                optional = cast(Reference1Parameters, _reference).get("optional")
                __builder.write(f'\n    .WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)})')
            elif _validate_type(_reference, ResourceWithServiceDiscovery):
                source = cast(ResourceWithServiceDiscovery, _reference)
                __builder.write(f'\n    .WithReference(source: {source.name})')
            elif _validate_type(_reference, ExternalServiceResource):
                external_service = cast(ExternalServiceResource, _reference)
                __builder.write(f'\n    .WithReference(externalService: {external_service.name})')
            elif _validate_tuple_types(_reference, (ResourceWithServiceDiscovery, str)):
                source, name, = cast(tuple[ResourceWithServiceDiscovery, str], _reference)
                __builder.write(f'\n    .WithReference(source: {source.name}, name: {_format_string(name, None)})')
            else:
                raise TypeError("Invalid type for option 'reference'")
        if _endpoint := kwargs.pop("endpoint", None):
            if _validate_dict_types(_endpoint, EndpointParameters):
                port = cast(EndpointParameters, _endpoint).get("port")
                target_port = cast(EndpointParameters, _endpoint).get("target_port")
                scheme = cast(EndpointParameters, _endpoint).get("scheme")
                name = cast(EndpointParameters, _endpoint).get("name")
                env = cast(EndpointParameters, _endpoint).get("env")
                is_proxied = cast(EndpointParameters, _endpoint).get("is_proxied")
                is_external = cast(EndpointParameters, _endpoint).get("is_external")
                protocol = cast(EndpointParameters, _endpoint).get("protocol")
                __builder.write(f'\n    .WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)})')
            elif _endpoint is True:
                __builder.write(f'\n    .WithEndpoint()')
            else:
                raise TypeError("Invalid type for option 'endpoint'")
        if _http_endpoint := kwargs.pop("http_endpoint", None):
            if _validate_dict_types(_http_endpoint, HttpEndpointParameters):
                port = cast(HttpEndpointParameters, _http_endpoint).get("port")
                target_port = cast(HttpEndpointParameters, _http_endpoint).get("target_port")
                name = cast(HttpEndpointParameters, _http_endpoint).get("name")
                env = cast(HttpEndpointParameters, _http_endpoint).get("env")
                is_proxied = cast(HttpEndpointParameters, _http_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _http_endpoint is True:
                __builder.write(f'\n    .WithHttpEndpoint()')
            else:
                raise TypeError("Invalid type for option 'http_endpoint'")
        if _https_endpoint := kwargs.pop("https_endpoint", None):
            if _validate_dict_types(_https_endpoint, HttpsEndpointParameters):
                port = cast(HttpsEndpointParameters, _https_endpoint).get("port")
                target_port = cast(HttpsEndpointParameters, _https_endpoint).get("target_port")
                name = cast(HttpsEndpointParameters, _https_endpoint).get("name")
                env = cast(HttpsEndpointParameters, _https_endpoint).get("env")
                is_proxied = cast(HttpsEndpointParameters, _https_endpoint).get("is_proxied")
                __builder.write(f'\n    .WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)})')
            elif _https_endpoint is True:
                __builder.write(f'\n    .WithHttpsEndpoint()')
            else:
                raise TypeError("Invalid type for option 'https_endpoint'")
        if _external_http_endpoints := kwargs.pop("external_http_endpoints", None):
            if _external_http_endpoints is True:
                __builder.write(f'\n    .WithExternalHttpEndpoints()')
            else:
                raise TypeError("Invalid type for option 'external_http_endpoints'")
        if _as_http2_service := kwargs.pop("as_http2_service", None):
            if _as_http2_service is True:
                __builder.write(f'\n    .AsHttp2Service()')
            else:
                raise TypeError("Invalid type for option 'as_http2_service'")
        if _wait_for := kwargs.pop("wait_for", None):
            if _validate_type(_wait_for, Resource):
                dependency = cast(Resource, _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for)
                __builder.write(f'\n    .WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for'")
        if _wait_for_start := kwargs.pop("wait_for_start", None):
            if _validate_type(_wait_for_start, Resource):
                dependency = cast(Resource, _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name})')
            elif _validate_tuple_types(_wait_for_start, (Resource, WaitBehavior)):
                dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], _wait_for_start)
                __builder.write(f'\n    .WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_start'")
        if _wait_for_completion := kwargs.pop("wait_for_completion", None):
            if _validate_type(_wait_for_completion, Resource):
                dependency = cast(Resource, _wait_for_completion)
                exit_code = None
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            elif _validate_tuple_types(_wait_for_completion, (Resource, int)):
                dependency, exit_code = cast(tuple[Resource, int], _wait_for_completion)
                __builder.write(f'\n    .WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)})')
            else:
                raise TypeError("Invalid type for option 'wait_for_completion'")
        if _http_health_check := kwargs.pop("http_health_check", None):
            if _validate_dict_types(_http_health_check, HttpHealthCheckParameters):
                path = cast(HttpHealthCheckParameters, _http_health_check).get("path")
                status_code = cast(HttpHealthCheckParameters, _http_health_check).get("status_code")
                endpoint_name = cast(HttpHealthCheckParameters, _http_health_check).get("endpoint_name")
                __builder.write(f'\n    .WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _http_health_check is True:
                __builder.write(f'\n    .WithHttpHealthCheck()')
            else:
                raise TypeError("Invalid type for option 'http_health_check'")
        if _http_command := kwargs.pop("http_command", None):
            if _validate_tuple_types(_http_command, (str, str)):
                path, display_name, = cast(tuple[str, str], _http_command)
                endpoint_name = None
                command_name = None
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            elif _validate_dict_types(_http_command, HttpCommandParameters):
                path = cast(HttpCommandParameters, _http_command)["path"]
                display_name = cast(HttpCommandParameters, _http_command)["display_name"]
                endpoint_name = cast(HttpCommandParameters, _http_command).get("endpoint_name")
                command_name = cast(HttpCommandParameters, _http_command).get("command_name")
                __builder.write(f'\n    .WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_command'")
        if _certificate_authority_collection := kwargs.pop("certificate_authority_collection", None):
            if _validate_type(_certificate_authority_collection, CertificateAuthorityCollection):
                certificate_authority_collection = cast(CertificateAuthorityCollection, _certificate_authority_collection)
                __builder.write(f'\n    .WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name})')
            else:
                raise TypeError("Invalid type for option 'certificate_authority_collection'")
        if _developer_certificate_trust := kwargs.pop("developer_certificate_trust", None):
            if _validate_type(_developer_certificate_trust, bool):
                trust = cast(bool, _developer_certificate_trust)
                __builder.write(f'\n    .WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)})')
            else:
                raise TypeError("Invalid type for option 'developer_certificate_trust'")
        if _certificate_trust_scope := kwargs.pop("certificate_trust_scope", None):
            if _validate_type(_certificate_trust_scope, CertificateTrustScope):
                scope = cast(CertificateTrustScope, _certificate_trust_scope)
                __builder.write(f'\n    .WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)})')
            else:
                raise TypeError("Invalid type for option 'certificate_trust_scope'")
        if _compute_env := kwargs.pop("compute_env", None):
            if _validate_type(_compute_env, ComputeEnvironmentResource):
                compute_env_resource = cast(ComputeEnvironmentResource, _compute_env)
                __builder.write(f'\n    .WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name})')
            else:
                raise TypeError("Invalid type for option 'compute_env'")
        if _http_probe := kwargs.pop("http_probe", None):
            if _validate_type(_http_probe, ProbeType):
                type = cast(ProbeType, _http_probe)
                path = None
                initial_delay_seconds = None
                period_seconds = None
                timeout_seconds = None
                failure_threshold = None
                success_threshold = None
                endpoint_name = None
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            elif _validate_dict_types(_http_probe, HttpProbeParameters):
                type = cast(HttpProbeParameters, _http_probe)["type"]
                path = cast(HttpProbeParameters, _http_probe).get("path")
                initial_delay_seconds = cast(HttpProbeParameters, _http_probe).get("initial_delay_seconds")
                period_seconds = cast(HttpProbeParameters, _http_probe).get("period_seconds")
                timeout_seconds = cast(HttpProbeParameters, _http_probe).get("timeout_seconds")
                failure_threshold = cast(HttpProbeParameters, _http_probe).get("failure_threshold")
                success_threshold = cast(HttpProbeParameters, _http_probe).get("success_threshold")
                endpoint_name = cast(HttpProbeParameters, _http_probe).get("endpoint_name")
                __builder.write(f'\n    .WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)})')
            else:
                raise TypeError("Invalid type for option 'http_probe'")
        super().__init__(__name, __builder, **kwargs)

    def publish_as_docker_file(self) -> Self:
        self._builder.write(f'\n{self.name}.PublishAsDockerFile();')
        return self

    def with_command(self, command: str, /) -> Self:
        if _validate_type(command, str):
            self._builder.write(f'\n{self.name}.WithCommand(command: {_format_string(command, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_working_dir(self, working_dir: str, /) -> Self:
        if _validate_type(working_dir, str):
            self._builder.write(f'\n{self.name}.WithWorkingDirectory(workingDirectory: {_format_string(working_dir, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_otlp_exporter(self) -> Self:
        ...
    @overload
    def with_otlp_exporter(self, protocol: OtlpProtocol, /) -> Self:
        ...
    def with_otlp_exporter(self, *args, **kwargs) -> Self:
        if not args and not kwargs:
            self._builder.write(f'\n{self.name}.WithOtlpExporter();')
            return self
        elif len(args) == 1 and _validate_type(args[0], OtlpProtocol):
            protocol = cast(OtlpProtocol, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with protocol")
            self._builder.write(f'\n{self.name}.WithOtlpExporter(protocol: {_format_enum("OtlpProtocol", protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_env(self, name: str, value: str | None, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_env(self, name: str, parameter: ParameterResource, /) -> Self:
        ...
    @overload
    def with_env(self, env_var_name: str, resource: ResourceWithConnectionString, /) -> Self:
        ...
    def with_env(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (), (str, str | None)):
            name, value, = cast(tuple[str, str], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, value: {_format_string(value, None)});')
            return self
        elif _validate_tuple_types(args + (), (str, ExternalServiceResource)):
            name, external_service, = cast(tuple[str, ExternalServiceResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ParameterResource)):
            name, parameter, = cast(tuple[str, ParameterResource], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(name: {_format_string(name, None)}, parameter: {parameter.name});')
            return self
        elif _validate_tuple_types(args + (), (str, ResourceWithConnectionString)):
            env_var_name, resource, = cast(tuple[str, ResourceWithConnectionString], args)
            self._builder.write(f'\n{self.name}.WithEnvironment(envVarName: {_format_string(env_var_name, None)}, resource: {resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_args(self, args: Iterable[str], /) -> Self:
        if _validate_type(args, Iterable[str]):
            self._builder.write(f'\n{self.name}.WithArgs(args: {_format_string_array(args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_reference_env(self, flags: ReferenceEnvironmentInjectionFlags, /) -> Self:
        if _validate_type(flags, ReferenceEnvironmentInjectionFlags):
            self._builder.write(f'\n{self.name}.WithReferenceEnvironment(flags: {_format_enum("ReferenceEnvironmentInjectionFlags", flags, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def with_reference(self, source: ResourceWithConnectionString, /, *, connection_name: str | None = None, optional: bool = False) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, /) -> Self:
        ...
    @overload
    def with_reference(self, external_service: ExternalServiceResource, /) -> Self:
        ...
    @overload
    def with_reference(self, source: ResourceWithServiceDiscovery, name: str, /) -> Self:
        ...
    def with_reference(self, *args, **kwargs) -> Self:
        if _validate_tuple_types(args + (_connection_name := kwargs.get("connection_name", None), _optional := kwargs.get("optional", False),), (ResourceWithConnectionString, str | None, bool | Literal[False])):
            source, = cast(tuple[ResourceWithConnectionString], args)
            connection_name = _connection_name
            optional = _optional
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, connectionName: {_format_string(connection_name, None)}, optional: {_format_bool(optional, False)});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ResourceWithServiceDiscovery):
            source = cast(ResourceWithServiceDiscovery, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with source")
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name});')
            return self
        elif len(args) == 1 and _validate_type(args[0], ExternalServiceResource):
            external_service = cast(ExternalServiceResource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with external_service")
            self._builder.write(f'\n{self.name}.WithReference(externalService: {external_service.name});')
            return self
        elif _validate_tuple_types(args + (), (ResourceWithServiceDiscovery, str)):
            source, name, = cast(tuple[ResourceWithServiceDiscovery, str], args)
            self._builder.write(f'\n{self.name}.WithReference(source: {source.name}, name: {_format_string(name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_endpoint(self, *, port: int | None = None, target_port: int | None = None, scheme: str | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True, is_external: bool | None = None, protocol: ProtocolType | None = None) -> Self:
        if _validate_tuple_types((port, target_port, scheme, name, env, is_proxied, is_external, protocol), (int | None, int | None, str | None, str | None, str | None, bool | Literal[True], bool | None, ProtocolType | None)):
            self._builder.write(f'\n{self.name}.WithEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, scheme: {_format_string(scheme, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)}, isExternal: {_format_value(is_external, None)}, protocol: {_format_value(protocol, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_https_endpoint(self, *, port: int | None = None, target_port: int | None = None, name: str | None = None, env: str | None = None, is_proxied: bool = True) -> Self:
        if _validate_tuple_types((port, target_port, name, env, is_proxied), (int | None, int | None, str | None, str | None, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithHttpsEndpoint(port: {_format_value(port, None)}, targetPort: {_format_value(target_port, None)}, name: {_format_string(name, None)}, env: {_format_string(env, None)}, isProxied: {_format_bool(is_proxied, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_external_http_endpoints(self) -> Self:
        self._builder.write(f'\n{self.name}.WithExternalHttpEndpoints();')
        return self

    def as_http2_service(self) -> Self:
        self._builder.write(f'\n{self.name}.AsHttp2Service();')
        return self

    @overload
    def wait_for(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitFor(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    @overload
    def wait_for_start(self, dependency: Resource, /) -> Self:
        ...
    @overload
    def wait_for_start(self, dependency: Resource, wait_behavior: WaitBehavior, /) -> Self:
        ...
    def wait_for_start(self, *args, **kwargs) -> Self:
        if len(args) == 1 and _validate_type(args[0], Resource):
            dependency = cast(Resource, args[0])
            if kwargs:
                raise TypeError(f"Keyword arguments not supported with dependency")
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name});')
            return self
        elif _validate_tuple_types(args + (), (Resource, WaitBehavior)):
            dependency, wait_behavior, = cast(tuple[Resource, WaitBehavior], args)
            self._builder.write(f'\n{self.name}.WaitForStart(dependency: {dependency.name}, waitBehavior: {_format_enum("WaitBehavior", wait_behavior, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def wait_for_completion(self, dependency: Resource, /, *, exit_code: int = 0) -> Self:
        if _validate_tuple_types((dependency, exit_code), (Resource, int | Literal[0])):
            self._builder.write(f'\n{self.name}.WaitForCompletion(dependency: {dependency.name}, exitCode: {_format_value(exit_code, 0)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_health_check(self, *, path: str | None = None, status_code: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((path, status_code, endpoint_name), (str | None, int | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpHealthCheck(path: {_format_string(path, None)}, statusCode: {_format_value(status_code, None)}, endpointName: {_format_string(endpoint_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_command(self, path: str, display_name: str, /, *, endpoint_name: str | None = None, command_name: str | None = None) -> Self:
        if _validate_tuple_types((path, display_name, endpoint_name, command_name), (str, str, str | None, str | None)):
            self._builder.write(f'\n{self.name}.WithHttpCommand(path: {_format_string(path, None)}, displayName: {_format_string(display_name, None)}, endpointName: {_format_string(endpoint_name, None)}, commandName: {_format_string(command_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_authority_collection(self, certificate_authority_collection: CertificateAuthorityCollection, /) -> Self:
        if _validate_type(certificate_authority_collection, CertificateAuthorityCollection):
            self._builder.write(f'\n{self.name}.WithCertificateAuthorityCollection(certificateAuthorityCollection: {certificate_authority_collection.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_developer_certificate_trust(self, trust: bool, /) -> Self:
        if _validate_type(trust, bool):
            self._builder.write(f'\n{self.name}.WithDeveloperCertificateTrust(trust: {_format_bool(trust, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_certificate_trust_scope(self, scope: CertificateTrustScope, /) -> Self:
        if _validate_type(scope, CertificateTrustScope):
            self._builder.write(f'\n{self.name}.WithCertificateTrustScope(scope: {_format_enum("CertificateTrustScope", scope, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_compute_env(self, compute_env_resource: ComputeEnvironmentResource, /) -> Self:
        if _validate_type(compute_env_resource, ComputeEnvironmentResource):
            self._builder.write(f'\n{self.name}.WithComputeEnvironment(computeEnvironmentResource: {compute_env_resource.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_http_probe(self, type: ProbeType, /, *, path: str | None = None, initial_delay_seconds: int | None = None, period_seconds: int | None = None, timeout_seconds: int | None = None, failure_threshold: int | None = None, success_threshold: int | None = None, endpoint_name: str | None = None) -> Self:
        if _validate_tuple_types((type, path, initial_delay_seconds, period_seconds, timeout_seconds, failure_threshold, success_threshold, endpoint_name), (ProbeType, str | None, int | None, int | None, int | None, int | None, int | None, str | None)):
            with _experimental(self._builder, "with_http_probe", self.__class__, "ASPIREPROBES001"):
                self._builder.write(f'\n{self.name}.WithHttpProbe(type: {_format_enum("ProbeType", type, None)}, path: {_format_string(path, None)}, initialDelaySeconds: {_format_value(initial_delay_seconds, None)}, periodSeconds: {_format_value(period_seconds, None)}, timeoutSeconds: {_format_value(timeout_seconds, None)}, failureThreshold: {_format_value(failure_threshold, None)}, successThreshold: {_format_value(success_threshold, None)}, endpointName: {_format_string(endpoint_name, None)});')
                return self
        else:
            raise TypeError("No matching overload found.")


class ParameterResourceOptions(_BaseResourceOptions, total=False):
    """Options for ParameterResource"""
    description: str | tuple[str, bool]


class ParameterResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[ParameterResourceOptions]) -> None:
        if _description := kwargs.pop("description", None):
            if _validate_type(_description, str):
                description = cast(str, _description)
                enable_markdown = None
                __builder.write(f'\n    .WithDescription(description: {_format_string(description, None)}, enableMarkdown: {_format_bool(enable_markdown, False)})')
            elif _validate_tuple_types(_description, (str, bool)):
                description, enable_markdown = cast(tuple[str, bool], _description)
                __builder.write(f'\n    .WithDescription(description: {_format_string(description, None)}, enableMarkdown: {_format_bool(enable_markdown, False)})')
            else:
                raise TypeError("Invalid type for option 'description'")
        super().__init__(__name, __builder, **kwargs)

    def with_description(self, description: str, /, *, enable_markdown: bool = False) -> Self:
        if _validate_tuple_types((description, enable_markdown), (str, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithDescription(description: {_format_string(description, None)}, enableMarkdown: {_format_bool(enable_markdown, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class PostgresDatabaseResourceOptions(_BaseResourceOptions, total=False):
    """Options for PostgresDatabaseResource"""
    creation_script: str
    connection_string_redirection: ResourceWithConnectionString


class PostgresDatabaseResource(_BaseResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.PostgreSQL@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[PostgresDatabaseResourceOptions]) -> None:
        if _creation_script := kwargs.pop("creation_script", None):
            if _validate_type(_creation_script, str):
                script = cast(str, _creation_script)
                __builder.write(f'\n    .WithCreationScript(script: {_format_string(script, None)})')
            else:
                raise TypeError("Invalid type for option 'creation_script'")
        if _connection_string_redirection := kwargs.pop("connection_string_redirection", None):
            if _validate_type(_connection_string_redirection, ResourceWithConnectionString):
                resource = cast(ResourceWithConnectionString, _connection_string_redirection)
                __builder.write(f'\n    .WithConnectionStringRedirection(resource: {_format_value(resource, None)})')
            else:
                raise TypeError("Invalid type for option 'connection_string_redirection'")
        super().__init__(__name, __builder, **kwargs)

    def with_creation_script(self, script: str, /) -> Self:
        if _validate_type(script, str):
            self._builder.write(f'\n{self.name}.WithCreationScript(script: {_format_string(script, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_connection_string_redirection(self, resource: ResourceWithConnectionString, /) -> Self:
        if _validate_type(resource, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithConnectionStringRedirection(resource: {_format_value(resource, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class PostgresServerResourceOptions(ContainerResourceOptions, total=False):
    """Options for PostgresServerResource"""
    pg_web: str | Literal[True]
    data_volume: DataVolumeParameters | Literal[True]
    data_bind_mount: str | tuple[str, bool]
    init_files: str
    password: ParameterResource
    user_name: ParameterResource
    host_port: int
    pg_admin: str | Literal[True]
    connection_string_redirection: ResourceWithConnectionString


class PostgresServerResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.PostgreSQL@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[PostgresServerResourceOptions]) -> None:
        if _pg_web := kwargs.pop("pg_web", None):
            if _validate_type(_pg_web, str):
                container_name = cast(str, _pg_web)
                container_name = None
                __builder.write(f'\n    .WithPgWeb(containerName: {_format_string(container_name, None)})')
            elif _pg_web is True:
                __builder.write(f'\n    .WithPgWeb()')
            else:
                raise TypeError("Invalid type for option 'pg_web'")
        if _data_volume := kwargs.pop("data_volume", None):
            if _validate_dict_types(_data_volume, DataVolumeParameters):
                name = cast(DataVolumeParameters, _data_volume).get("name")
                is_read_only = cast(DataVolumeParameters, _data_volume).get("is_read_only")
                __builder.write(f'\n    .WithDataVolume(name: {_format_string(name, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _data_volume is True:
                __builder.write(f'\n    .WithDataVolume()')
            else:
                raise TypeError("Invalid type for option 'data_volume'")
        if _data_bind_mount := kwargs.pop("data_bind_mount", None):
            if _validate_type(_data_bind_mount, str):
                source = cast(str, _data_bind_mount)
                is_read_only = None
                __builder.write(f'\n    .WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _validate_tuple_types(_data_bind_mount, (str, bool)):
                source, is_read_only = cast(tuple[str, bool], _data_bind_mount)
                __builder.write(f'\n    .WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            else:
                raise TypeError("Invalid type for option 'data_bind_mount'")
        if _init_files := kwargs.pop("init_files", None):
            if _validate_type(_init_files, str):
                source = cast(str, _init_files)
                __builder.write(f'\n    .WithInitFiles(source: {_format_string(source, None)})')
            else:
                raise TypeError("Invalid type for option 'init_files'")
        if _password := kwargs.pop("password", None):
            if _validate_type(_password, ParameterResource):
                password = cast(ParameterResource, _password)
                __builder.write(f'\n    .WithPassword(password: {password.name})')
            else:
                raise TypeError("Invalid type for option 'password'")
        if _user_name := kwargs.pop("user_name", None):
            if _validate_type(_user_name, ParameterResource):
                user_name = cast(ParameterResource, _user_name)
                __builder.write(f'\n    .WithUserName(userName: {user_name.name})')
            else:
                raise TypeError("Invalid type for option 'user_name'")
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        if _pg_admin := kwargs.pop("pg_admin", None):
            if _validate_type(_pg_admin, str):
                container_name = cast(str, _pg_admin)
                container_name = None
                __builder.write(f'\n    .WithPgAdmin(containerName: {_format_string(container_name, None)})')
            elif _pg_admin is True:
                __builder.write(f'\n    .WithPgAdmin()')
            else:
                raise TypeError("Invalid type for option 'pg_admin'")
        if _connection_string_redirection := kwargs.pop("connection_string_redirection", None):
            if _validate_type(_connection_string_redirection, ResourceWithConnectionString):
                resource = cast(ResourceWithConnectionString, _connection_string_redirection)
                __builder.write(f'\n    .WithConnectionStringRedirection(resource: {_format_value(resource, None)})')
            else:
                raise TypeError("Invalid type for option 'connection_string_redirection'")
        super().__init__(__name, __builder, **kwargs)

    def add_database(self, name: str, /, database_name: str | None = None, **kwargs: Unpack[PostgresDatabaseResourceOptions]) -> PostgresDatabaseResource:
        with _check_warnings(self._builder, kwargs, PostgresDatabaseResourceOptions, "AddDatabase"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = {self.name}.AddDatabase(name: {_format_string(name, None)}, databaseName: {_format_string(database_name, None)})')
            result = PostgresDatabaseResource(var_name, self._builder, **kwargs)
            return result

    def with_pg_web(self, *, container_name: str | None = None) -> Self:
        if _validate_type(container_name, str | None):
            container_name = None
            self._builder.write(f'\n{self.name}.WithPgWeb(containerName: {_format_string(container_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_volume(self, *, name: str | None = None, is_read_only: bool = False) -> Self:
        if _validate_tuple_types((name, is_read_only), (str | None, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithDataVolume(name: {_format_string(name, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_bind_mount(self, source: str, /, *, is_read_only: bool = False) -> Self:
        if _validate_tuple_types((source, is_read_only), (str, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_init_files(self, source: str, /) -> Self:
        if _validate_type(source, str):
            self._builder.write(f'\n{self.name}.WithInitFiles(source: {_format_string(source, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_password(self, password: ParameterResource, /) -> Self:
        if _validate_type(password, ParameterResource):
            self._builder.write(f'\n{self.name}.WithPassword(password: {password.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_user_name(self, user_name: ParameterResource, /) -> Self:
        if _validate_type(user_name, ParameterResource):
            self._builder.write(f'\n{self.name}.WithUserName(userName: {user_name.name});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_pg_admin(self, *, container_name: str | None = None) -> Self:
        if _validate_type(container_name, str | None):
            container_name = None
            self._builder.write(f'\n{self.name}.WithPgAdmin(containerName: {_format_string(container_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_connection_string_redirection(self, resource: ResourceWithConnectionString, /) -> Self:
        if _validate_type(resource, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithConnectionStringRedirection(resource: {_format_value(resource, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class PgAdminContainerResourceOptions(ContainerResourceOptions, total=False):
    """Options for PgAdminContainerResource"""
    host_port: int


class PgAdminContainerResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.PostgreSQL@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[PgAdminContainerResourceOptions]) -> None:
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        super().__init__(__name, __builder, **kwargs)

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class PgWebContainerResourceOptions(ContainerResourceOptions, total=False):
    """Options for PgWebContainerResource"""
    host_port: int


class PgWebContainerResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.PostgreSQL@13.0.1.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[PgWebContainerResourceOptions]) -> None:
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        super().__init__(__name, __builder, **kwargs)

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class PythonAppResourceOptions(ExecutableResourceOptions, total=False):
    """Options for PythonAppResource"""
    virtual_env: str | tuple[str, bool]
    debugging: Literal[True]
    entrypoint: tuple[EntrypointType, str]
    pip: PipParameters | Literal[True]
    uv: UvParameters | Literal[True]
    publish_with_container_files: tuple[ResourceWithContainerFiles, str]


class PythonAppResource(ExecutableResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.Python@13.0.0.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[PythonAppResourceOptions]) -> None:
        if _virtual_env := kwargs.pop("virtual_env", None):
            if _validate_type(_virtual_env, str):
                virtual_env_path = cast(str, _virtual_env)
                create_if_not_exists = None
                __builder.write(f'\n    .WithVirtualEnvironment(virtualEnvironmentPath: {_format_string(virtual_env_path, None)}, createIfNotExists: {_format_bool(create_if_not_exists, True)})')
            elif _validate_tuple_types(_virtual_env, (str, bool)):
                virtual_env_path, create_if_not_exists = cast(tuple[str, bool], _virtual_env)
                __builder.write(f'\n    .WithVirtualEnvironment(virtualEnvironmentPath: {_format_string(virtual_env_path, None)}, createIfNotExists: {_format_bool(create_if_not_exists, True)})')
            else:
                raise TypeError("Invalid type for option 'virtual_env'")
        if _debugging := kwargs.pop("debugging", None):
            if _debugging is True:
                __builder.write(f'\n    .WithDebugging()')
            else:
                raise TypeError("Invalid type for option 'debugging'")
        if _entrypoint := kwargs.pop("entrypoint", None):
            if _validate_tuple_types(_entrypoint, (EntrypointType, str)):
                entrypoint_type, entrypoint, = cast(tuple[EntrypointType, str], _entrypoint)
                __builder.write(f'\n    .WithEntrypoint(entrypointType: {_format_enum("EntrypointType", entrypoint_type, None)}, entrypoint: {_format_string(entrypoint, None)})')
            else:
                raise TypeError("Invalid type for option 'entrypoint'")
        if _pip := kwargs.pop("pip", None):
            if _validate_dict_types(_pip, PipParameters):
                install = cast(PipParameters, _pip).get("install")
                install_args = cast(PipParameters, _pip).get("install_args")
                __builder.write(f'\n    .WithPip(install: {_format_bool(install, True)}, installArgs: {_format_string_array(install_args)})')
            elif _pip is True:
                __builder.write(f'\n    .WithPip()')
            else:
                raise TypeError("Invalid type for option 'pip'")
        if _uv := kwargs.pop("uv", None):
            if _validate_dict_types(_uv, UvParameters):
                install = cast(UvParameters, _uv).get("install")
                args = cast(UvParameters, _uv).get("args")
                __builder.write(f'\n    .WithUv(install: {_format_bool(install, True)}, args: {_format_string_array(args)})')
            elif _uv is True:
                __builder.write(f'\n    .WithUv()')
            else:
                raise TypeError("Invalid type for option 'uv'")
        if _publish_with_container_files := kwargs.pop("publish_with_container_files", None):
            if _validate_tuple_types(_publish_with_container_files, (ResourceWithContainerFiles, str)):
                source, destination_path, = cast(tuple[ResourceWithContainerFiles, str], _publish_with_container_files)
                __builder.write(f'\n    .PublishWithContainerFiles(source: {source.name}, destinationPath: {_format_string(destination_path, None)})')
            else:
                raise TypeError("Invalid type for option 'publish_with_container_files'")
        super().__init__(__name, __builder, **kwargs)

    def with_virtual_env(self, virtual_env_path: str, /, *, create_if_not_exists: bool = True) -> Self:
        if _validate_tuple_types((virtual_env_path, create_if_not_exists), (str, bool | Literal[True])):
            self._builder.write(f'\n{self.name}.WithVirtualEnvironment(virtualEnvironmentPath: {_format_string(virtual_env_path, None)}, createIfNotExists: {_format_bool(create_if_not_exists, True)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_debugging(self) -> Self:
        self._builder.write(f'\n{self.name}.WithDebugging();')
        return self

    def with_entrypoint(self, entrypoint_type: EntrypointType, entrypoint: str, /) -> Self:
        if _validate_tuple_types((entrypoint_type, entrypoint, ), (EntrypointType, str)):
            self._builder.write(f'\n{self.name}.WithEntrypoint(entrypointType: {_format_enum("EntrypointType", entrypoint_type, None)}, entrypoint: {_format_string(entrypoint, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_pip(self, *, install: bool = True, install_args: Iterable[str] | None = None) -> Self:
        if _validate_tuple_types((install, install_args), (bool | Literal[True], Iterable[str] | None)):
            self._builder.write(f'\n{self.name}.WithPip(install: {_format_bool(install, True)}, installArgs: {_format_string_array(install_args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_uv(self, *, install: bool = True, args: Iterable[str] | None = None) -> Self:
        if _validate_tuple_types((install, args), (bool | Literal[True], Iterable[str] | None)):
            self._builder.write(f'\n{self.name}.WithUv(install: {_format_bool(install, True)}, args: {_format_string_array(args)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def publish_with_container_files(self, source: ResourceWithContainerFiles, destination_path: str, /) -> Self:
        if _validate_tuple_types((source, destination_path, ), (ResourceWithContainerFiles, str)):
            self._builder.write(f'\n{self.name}.PublishWithContainerFiles(source: {source.name}, destinationPath: {_format_string(destination_path, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class UvicornAppResourceOptions(PythonAppResourceOptions, total=False):
    """Options for UvicornAppResource"""


class UvicornAppResource(PythonAppResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.Python@13.0.0.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[UvicornAppResourceOptions]) -> None:
        super().__init__(__name, __builder, **kwargs)


class RedisResourceOptions(ContainerResourceOptions, total=False):
    """Options for RedisResource"""
    redis_commander: str | Literal[True]
    redis_insight: str | Literal[True]
    data_volume: DataVolumeParameters | Literal[True]
    data_bind_mount: str | tuple[str, bool]
    persistence: PersistenceParameters | Literal[True]
    password: ParameterResource
    host_port: int
    connection_string_redirection: ResourceWithConnectionString


class RedisResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.Redis@13.0.0.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[RedisResourceOptions]) -> None:
        if _redis_commander := kwargs.pop("redis_commander", None):
            if _validate_type(_redis_commander, str):
                container_name = cast(str, _redis_commander)
                container_name = None
                __builder.write(f'\n    .WithRedisCommander(containerName: {_format_string(container_name, None)})')
            elif _redis_commander is True:
                __builder.write(f'\n    .WithRedisCommander()')
            else:
                raise TypeError("Invalid type for option 'redis_commander'")
        if _redis_insight := kwargs.pop("redis_insight", None):
            if _validate_type(_redis_insight, str):
                container_name = cast(str, _redis_insight)
                container_name = None
                __builder.write(f'\n    .WithRedisInsight(containerName: {_format_string(container_name, None)})')
            elif _redis_insight is True:
                __builder.write(f'\n    .WithRedisInsight()')
            else:
                raise TypeError("Invalid type for option 'redis_insight'")
        if _data_volume := kwargs.pop("data_volume", None):
            if _validate_dict_types(_data_volume, DataVolumeParameters):
                name = cast(DataVolumeParameters, _data_volume).get("name")
                is_read_only = cast(DataVolumeParameters, _data_volume).get("is_read_only")
                __builder.write(f'\n    .WithDataVolume(name: {_format_string(name, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _data_volume is True:
                __builder.write(f'\n    .WithDataVolume()')
            else:
                raise TypeError("Invalid type for option 'data_volume'")
        if _data_bind_mount := kwargs.pop("data_bind_mount", None):
            if _validate_type(_data_bind_mount, str):
                source = cast(str, _data_bind_mount)
                is_read_only = None
                __builder.write(f'\n    .WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            elif _validate_tuple_types(_data_bind_mount, (str, bool)):
                source, is_read_only = cast(tuple[str, bool], _data_bind_mount)
                __builder.write(f'\n    .WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)})')
            else:
                raise TypeError("Invalid type for option 'data_bind_mount'")
        if _persistence := kwargs.pop("persistence", None):
            if _validate_dict_types(_persistence, PersistenceParameters):
                interval = cast(PersistenceParameters, _persistence).get("interval")
                keys_changed_threshold = cast(PersistenceParameters, _persistence).get("keys_changed_threshold")
                __builder.write(f'\n    .WithPersistence(interval: {_format_value(interval, None)}, keysChangedThreshold: {_format_value(keys_changed_threshold, 1)})')
            elif _persistence is True:
                __builder.write(f'\n    .WithPersistence()')
            else:
                raise TypeError("Invalid type for option 'persistence'")
        if _password := kwargs.pop("password", None):
            if _validate_type(_password, ParameterResource):
                password = cast(ParameterResource, _password)
                __builder.write(f'\n    .WithPassword(password: {password.name if password else "null"})')
            else:
                raise TypeError("Invalid type for option 'password'")
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        if _connection_string_redirection := kwargs.pop("connection_string_redirection", None):
            if _validate_type(_connection_string_redirection, ResourceWithConnectionString):
                resource = cast(ResourceWithConnectionString, _connection_string_redirection)
                __builder.write(f'\n    .WithConnectionStringRedirection(resource: {_format_value(resource, None)})')
            else:
                raise TypeError("Invalid type for option 'connection_string_redirection'")
        super().__init__(__name, __builder, **kwargs)

    def with_redis_commander(self, *, container_name: str | None = None) -> Self:
        if _validate_type(container_name, str | None):
            container_name = None
            self._builder.write(f'\n{self.name}.WithRedisCommander(containerName: {_format_string(container_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_redis_insight(self, *, container_name: str | None = None) -> Self:
        if _validate_type(container_name, str | None):
            container_name = None
            self._builder.write(f'\n{self.name}.WithRedisInsight(containerName: {_format_string(container_name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_volume(self, *, name: str | None = None, is_read_only: bool = False) -> Self:
        if _validate_tuple_types((name, is_read_only), (str | None, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithDataVolume(name: {_format_string(name, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_bind_mount(self, source: str, /, *, is_read_only: bool = False) -> Self:
        if _validate_tuple_types((source, is_read_only), (str, bool | Literal[False])):
            self._builder.write(f'\n{self.name}.WithDataBindMount(source: {_format_string(source, None)}, isReadOnly: {_format_bool(is_read_only, False)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_persistence(self, *, interval: timedelta | None = None, keys_changed_threshold: int = 1) -> Self:
        if _validate_tuple_types((interval, keys_changed_threshold), (timedelta | None, int | Literal[1])):
            self._builder.write(f'\n{self.name}.WithPersistence(interval: {_format_value(interval, None)}, keysChangedThreshold: {_format_value(keys_changed_threshold, 1)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_password(self, password: ParameterResource | None, /) -> Self:
        if _validate_type(password, ParameterResource | None):
            self._builder.write(f'\n{self.name}.WithPassword(password: {password.name if password else "null"});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_connection_string_redirection(self, resource: ResourceWithConnectionString, /) -> Self:
        if _validate_type(resource, ResourceWithConnectionString):
            self._builder.write(f'\n{self.name}.WithConnectionStringRedirection(resource: {_format_value(resource, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class RedisCommanderResourceOptions(ContainerResourceOptions, total=False):
    """Options for RedisCommanderResource"""
    host_port: int


class RedisCommanderResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.Redis@13.0.0.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[RedisCommanderResourceOptions]) -> None:
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        super().__init__(__name, __builder, **kwargs)

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class RedisInsightResourceOptions(ContainerResourceOptions, total=False):
    """Options for RedisInsightResource"""
    host_port: int
    data_volume: str | Literal[True]
    data_bind_mount: str


class RedisInsightResource(ContainerResource):
    @property
    def package(self) -> str:
        return "#:package Aspire.Hosting.Redis@13.0.0.0"

    def __init__(self, __name: str, __builder: StringIO, **kwargs: Unpack[RedisInsightResourceOptions]) -> None:
        if _host_port := kwargs.pop("host_port", None):
            if _validate_type(_host_port, int):
                port = cast(int, _host_port)
                __builder.write(f'\n    .WithHostPort(port: {_format_value(port, None)})')
            else:
                raise TypeError("Invalid type for option 'host_port'")
        if _data_volume := kwargs.pop("data_volume", None):
            if _validate_type(_data_volume, str):
                name = cast(str, _data_volume)
                name = None
                __builder.write(f'\n    .WithDataVolume(name: {_format_string(name, None)})')
            elif _data_volume is True:
                __builder.write(f'\n    .WithDataVolume()')
            else:
                raise TypeError("Invalid type for option 'data_volume'")
        if _data_bind_mount := kwargs.pop("data_bind_mount", None):
            if _validate_type(_data_bind_mount, str):
                source = cast(str, _data_bind_mount)
                __builder.write(f'\n    .WithDataBindMount(source: {_format_string(source, None)})')
            else:
                raise TypeError("Invalid type for option 'data_bind_mount'")
        super().__init__(__name, __builder, **kwargs)

    def with_host_port(self, port: int | None = None, /) -> Self:
        if _validate_type(port, int):
            self._builder.write(f'\n{self.name}.WithHostPort(port: {_format_value(port, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_volume(self, *, name: str | None = None) -> Self:
        if _validate_type(name, str | None):
            name = None
            self._builder.write(f'\n{self.name}.WithDataVolume(name: {_format_string(name, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")

    def with_data_bind_mount(self, source: str, /) -> Self:
        if _validate_type(source, str):
            self._builder.write(f'\n{self.name}.WithDataBindMount(source: {_format_string(source, None)});')
            return self
        else:
            raise TypeError("No matching overload found.")


class DistributedApplication:

    def __init__(self, apphost_path: Path) -> None:
        self.apphost_path = apphost_path

    def run(self) -> None:
        '''Runs the distributed application.'''
        pass


class DistributedApplicationBuilder:
    def __init__(self, *args) -> None:
        self._dependencies = []
        self._builder = StringIO()
        self._builder.write("var builder = DistributedApplication.CreateBuilder(args);\n")

    def build(self, *, output_dir: str | None = None) -> DistributedApplication:
        csharp = self._builder.getvalue()
        csharp += "\n\nbuilder.Build().Run();\n"
        csharp = (
            f"#:sdk Aspire.AppHost.Sdk@{__VERSION__}\n" +
            "\n".join(set(sorted(self._dependencies))) +
            "\nusing System.Security.Cryptography.X509Certificates;" +
            "\n\n" + csharp
        )
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            with open(output_path / "apphost.cs", "w", encoding="utf-8") as f:
                f.write(csharp)
        else:
            cwd = Path.cwd()
            output_path = cwd / ".aspire" / "aspyre_apphost"
            output_path.mkdir(parents=True, exist_ok=True)
            with open(output_path / "apphost.cs", "w", encoding="utf-8") as f:
                f.write(csharp)
        return DistributedApplication(apphost_path=output_path / "apphost.cs")

    def add_connection_string(self, name: str, /, *, env_var_name: str | None = None, **kwargs: Unpack[ConnectionStringResourceOptions]) -> ResourceWithConnectionString:
        with _check_warnings(self._builder, kwargs, ConnectionStringResourceOptions, "add_connection_string"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddConnectionString(name: {_format_string(name, None)}, environmentVariableName: {_format_string(env_var_name, None)})')
            result = ConnectionStringResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    @overload
    def add_container(self, name: str, image: str, /, **kwargs: Unpack[ContainerResourceOptions]) -> ContainerResource:
        ...
    @overload
    def add_container(self, name: str, image: str, tag: str, /, **kwargs: Unpack[ContainerResourceOptions]) -> ContainerResource:
        ...
    def add_container(self, *args, **kwargs):
        if _validate_tuple_types(args, (str, str,)):
            with _check_warnings(self._builder, kwargs, ContainerResourceOptions, "add_container"):
                name, image, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddContainer(name: {_format_string(name, None)}, image: {_format_string(image, None)})')
                result = ContainerResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        if _validate_tuple_types(args, (str, str, str,)):
            with _check_warnings(self._builder, kwargs, ContainerResourceOptions, "add_container"):
                name, image, tag, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddContainer(name: {_format_string(name, None)}, image: {_format_string(image, None)}, tag: {_format_string(tag, None)})')
                result = ContainerResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        raise TypeError("No matching overload found.")

    def add_dockerfile(self, name: str, context_path: str, /, *, dockerfile_path: str | None = None, stage: str | None = None, **kwargs: Unpack[ContainerResourceOptions]) -> ContainerResource:
        with _check_warnings(self._builder, kwargs, ContainerResourceOptions, "add_dockerfile"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddDockerfile(name: {_format_string(name, None)}, contextPath: {_format_string(context_path, None)}, dockerfilePath: {_format_string(dockerfile_path, None)}, stage: {_format_string(stage, None)})')
            result = ContainerResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_executable(self, name: str, command: str, working_dir: str, args: Iterable[str] | None, /, **kwargs: Unpack[ExecutableResourceOptions]) -> ExecutableResource:
        with _check_warnings(self._builder, kwargs, ExecutableResourceOptions, "add_executable"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddExecutable(name: {_format_string(name, None)}, command: {_format_string(command, None)}, workingDirectory: {_format_string(working_dir, None)}, args: {_format_string_array(args)})')
            result = ExecutableResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    @overload
    def add_external_service(self, name: str, url: str, /, **kwargs: Unpack[ExternalServiceResourceOptions]) -> ExternalServiceResource:
        ...
    @overload
    def add_external_service(self, name: str, url_parameter: ParameterResource, /, **kwargs: Unpack[ExternalServiceResourceOptions]) -> ExternalServiceResource:
        ...
    def add_external_service(self, *args, **kwargs):
        if _validate_tuple_types(args, (str, str,)):
            with _check_warnings(self._builder, kwargs, ExternalServiceResourceOptions, "add_external_service"):
                name, url, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddExternalService(name: {_format_string(name, None)}, url: {_format_string(url, None)})')
                result = ExternalServiceResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        if _validate_tuple_types(args, (str, ParameterResource,)):
            with _check_warnings(self._builder, kwargs, ExternalServiceResourceOptions, "add_external_service"):
                name, url_parameter, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddExternalService(name: {_format_string(name, None)}, urlParameter: {url_parameter.name})')
                result = ExternalServiceResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        raise TypeError("No matching overload found.")

    @overload
    def add_parameter(self, name: str, /, *, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        ...
    @overload
    def add_parameter(self, name: str, value: str, /, *, publish_value_as_default: bool = False, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        ...
    def add_parameter(self, *args, **kwargs):
        if _validate_tuple_types(args, (str,)):
            with _check_warnings(self._builder, kwargs, ParameterResourceOptions, "add_parameter"):
                name, = args
                var_name = _valid_var_name(name)
                secret = kwargs.pop("secret", None)
                self._builder.write(f'\nvar {var_name} = builder.AddParameter(name: {_format_string(name, None)}, secret: {_format_bool(secret, False)})')
                result = ParameterResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        if _validate_tuple_types(args, (str, str,)):
            with _check_warnings(self._builder, kwargs, ParameterResourceOptions, "add_parameter"):
                name, value, = args
                var_name = _valid_var_name(name)
                publish_value_as_default = kwargs.pop("publish_value_as_default", None)
                secret = kwargs.pop("secret", None)
                self._builder.write(f'\nvar {var_name} = builder.AddParameter(name: {_format_string(name, None)}, value: {_format_string(value, None)}, publishValueAsDefault: {_format_bool(publish_value_as_default, False)}, secret: {_format_bool(secret, False)})')
                result = ParameterResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        raise TypeError("No matching overload found.")

    def add_parameter_from_config(self, name: str, config_key: str, /, *, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        with _check_warnings(self._builder, kwargs, ParameterResourceOptions, "add_parameter_from_config"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddParameterFromConfiguration(name: {_format_string(name, None)}, configurationKey: {_format_string(config_key, None)}, secret: {_format_bool(secret, False)})')
            result = ParameterResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    @overload
    def add_project(self, name: str, project_path: str, /, **kwargs: Unpack[ProjectResourceOptions]) -> ProjectResource:
        ...
    @overload
    def add_project(self, name: str, project_path: str, launch_profile_name: str | None, /, **kwargs: Unpack[ProjectResourceOptions]) -> ProjectResource:
        ...
    def add_project(self, *args, **kwargs):
        if _validate_tuple_types(args, (str, str,)):
            with _check_warnings(self._builder, kwargs, ProjectResourceOptions, "add_project"):
                name, project_path, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddProject(name: {_format_string(name, None)}, projectPath: {_format_string(project_path, None)})')
                result = ProjectResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        if _validate_tuple_types(args, (str, str, str,)):
            with _check_warnings(self._builder, kwargs, ProjectResourceOptions, "add_project"):
                name, project_path, launch_profile_name, = args
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddProject(name: {_format_string(name, None)}, projectPath: {_format_string(project_path, None)}, launchProfileName: {_format_string(launch_profile_name, None)})')
                result = ProjectResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result
        raise TypeError("No matching overload found.")

    def add_csharp_app(self, name: str, path: str, /, **kwargs: Unpack[ProjectResourceOptions]) -> ProjectResource:
        with _experimental(self._builder, "add_csharp_app", self.__class__, "ASPIRECSHARPAPPS001"):
            with _check_warnings(self._builder, kwargs, ProjectResourceOptions, "add_csharp_app"):
                var_name = _valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddCSharpApp(name: {_format_string(name, None)}, path: {_format_string(path, None)})')
                result = ProjectResource(var_name, self._builder, **kwargs)
                self._dependencies.append(result.package)
                return result

    def add_certificate_authority_collection(self, name: str, /, **kwargs: Unpack[CertificateAuthorityCollectionOptions]) -> CertificateAuthorityCollection:
        with _check_warnings(self._builder, kwargs, CertificateAuthorityCollectionOptions, "add_certificate_authority_collection"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddCertificateAuthorityCollection(name: {_format_string(name, None)})')
            result = CertificateAuthorityCollection(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_postgres(self, name: str, /, *, port: int | None = None, **kwargs: Unpack[PostgresServerResourceOptions]) -> PostgresServerResource:
        with _check_warnings(self._builder, kwargs, PostgresServerResourceOptions, "add_postgres"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddPostgres(name: {_format_string(name, None)}, port: {_format_value(port, None)})')
            result = PostgresServerResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_python_app(self, name: str, app_dir: str, script_path: str, /, **kwargs: Unpack[PythonAppResourceOptions]) -> PythonAppResource:
        with _check_warnings(self._builder, kwargs, PythonAppResourceOptions, "add_python_app"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddPythonApp(name: {_format_string(name, None)}, appDirectory: {_format_string(app_dir, None)}, scriptPath: {_format_string(script_path, None)})')
            result = PythonAppResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_python_module(self, name: str, app_dir: str, module_name: str, /, **kwargs: Unpack[PythonAppResourceOptions]) -> PythonAppResource:
        with _check_warnings(self._builder, kwargs, PythonAppResourceOptions, "add_python_module"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddPythonModule(name: {_format_string(name, None)}, appDirectory: {_format_string(app_dir, None)}, moduleName: {_format_string(module_name, None)})')
            result = PythonAppResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_python_executable(self, name: str, app_dir: str, executable_name: str, /, **kwargs: Unpack[PythonAppResourceOptions]) -> PythonAppResource:
        with _check_warnings(self._builder, kwargs, PythonAppResourceOptions, "add_python_executable"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddPythonExecutable(name: {_format_string(name, None)}, appDirectory: {_format_string(app_dir, None)}, executableName: {_format_string(executable_name, None)})')
            result = PythonAppResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_uvicorn_app(self, name: str, app_dir: str, app: str, /, **kwargs: Unpack[UvicornAppResourceOptions]) -> UvicornAppResource:
        with _check_warnings(self._builder, kwargs, UvicornAppResourceOptions, "add_uvicorn_app"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddUvicornApp(name: {_format_string(name, None)}, appDirectory: {_format_string(app_dir, None)}, app: {_format_string(app, None)})')
            result = UvicornAppResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result

    def add_redis(self, name: str, /, *, port: int | None = None, **kwargs: Unpack[RedisResourceOptions]) -> RedisResource:
        with _check_warnings(self._builder, kwargs, RedisResourceOptions, "add_redis"):
            var_name = _valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddRedis(name: {_format_string(name, None)}, port: {_format_value(port, None)})')
            result = RedisResource(var_name, self._builder, **kwargs)
            self._dependencies.append(result.package)
            return result


def build_distributed_application(*args) -> DistributedApplicationBuilder:
    return DistributedApplicationBuilder(*args)
