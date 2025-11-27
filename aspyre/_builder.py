#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from typing import Iterable, TypedDict, overload
from typing_extensions import Unpack
from io import StringIO
import pathlib

from ._utils import valid_var_name, format_bool, format_string, format_string_array, get_nullable_value
from ._annotations import check_warnings, experimental
from .resources._base import (
    CSharpAppResource,
    CertificateAuthorityCollection,
    CertificateAuthorityCollectionOptions,
    ContainerResource,
    ContainerResourceOptions,
    ExecutableResource,
    ExecutableResourceOptions,
    ExternalServiceResource,
    ResourceOptions,
    ConnectionStringResource,
    ConnectionStringResourceOptions,
    ProjectResource,
    ProjectResourceOptions,
    ParameterResource,
    ParameterResourceOptions,
)


class DistributedApplicationOptions(TypedDict, total=False):
    AllowUnsecuredTransport: bool
    """Allows the use of HTTP urls for for the AppHost resource endpoint."""
    Args: Iterable[str]
    """The command line arguments."""
    ContainerRegistryOverride: str
    """When containers are used, use this value instead to override the container registry that is specified."""
    DashboardApplicationName: str
    """The application name to display in the dashboard. For file-based app hosts, this defaults to the directory name. For other apps, it falls back to the environment's application name."""
    DisableDashboard: bool
    """Determines whether the dashboard is disabled."""
    EnableResourceLogging: bool
    """Enables resource logging. Logs will be written to the logger category (ApplicationName.Resources.{resourceName})."""
    ProjectDirectory: str
    """The directory containing the AppHost project file. If not set, defaults to the directory resolved from assembly metadata."""
    TrustDeveloperCertificate: bool
    """Whether to attempt to implicitly add trust for developer certificates (currently the ASP.NET developer certificate) by default at runtime."""


class _DistributedApplicationBuilder:
    version: str = "13.0.0"

    def __init__(self, *args) -> None:
        self._dependencies = []
        self._builder = StringIO()
        self._builder.write("var builder = DistributedApplication.CreateBuilder(args);\n")

    def build(self, *, output_dir: str | None = None, name: str | None = None) -> str:
        csharp = self._builder.getvalue()
        csharp += "\n\nbuilder.Build().Run();\n"
        csharp = (
            f"#:sdk Aspire.AppHost.Sdk@{self.version}\n" +
            "\n".join(set(sorted([d if d.endswith(';') else f"{d}@{self.version}" for dependency in self._dependencies for d in dependency]))) +
            "\n\n" + csharp
        )
        if output_dir:
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            with open(output_path / "apphost.cs", "w", encoding="utf-8") as f:
                f.write(csharp)
        else:
            cwd = pathlib.Path.cwd()
            output_path = cwd / ".aspire" / "aspyre_apphost"
            output_path.mkdir(parents=True, exist_ok=True)
            with open(output_path / "apphost.cs", "w", encoding="utf-8") as f:
                f.write(csharp)
        return csharp

    @overload
    def add_parameter(self, name: str, /,*, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        ...
    @overload
    def add_parameter(
        self,
        name: str,
        value: str,
        /, *,
        publish_value_as_default: bool = False,
        secret: bool = False,
        **kwargs: Unpack[ParameterResourceOptions]
    ) -> ParameterResource:
        ...
    def add_parameter(self, *args, **kwargs):
        with check_warnings(self._builder, kwargs, ParameterResourceOptions, "add_parameter"):
            var_name = valid_var_name(args[0])
            name = args[0]
            secret = kwargs.pop("secret", False)
            publish_value_as_default = kwargs.pop("publish_value_as_default", False)
            if len(args) ==1:
                self._builder.write(f'\nvar {var_name} = builder.AddParameter("{name}", {format_bool(secret)})')
            else:
                self._builder.write(f'\nvar {var_name} = builder.AddParameter("{name}", {format_string(args[1])}, {format_bool(publish_value_as_default)}, {format_bool(secret)})')
            result = ParameterResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_parameter_from_configuration(self, name: str, configuration_key: str, /, *, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        with check_warnings(self._builder, kwargs, ParameterResourceOptions, "add_parameter_from_configuration"):
            var_name = valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddParameterFromConfiguration({format_string(name)},  {format_string(configuration_key)}, {format_bool(secret)})')
            result = ParameterResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_connection_string(self, name: str, /, *, env_var: str | None = None, **kwargs: Unpack[ConnectionStringResourceOptions]) -> ConnectionStringResource:
        with check_warnings(self._builder, kwargs, ConnectionStringResourceOptions, "add_connection_string"):
            var_name = valid_var_name(name)
            if env_var:
                self._builder.write(f'\nvar {var_name} = builder.AddConnectionString({format_string(name)}, {format_string(env_var)})')
            else:
                self._builder.write(f'\nvar {var_name} = builder.AddConnectionString({format_string(name)})')
            result = ConnectionStringResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_container(self, name: str, image: str, /, *, tag: str | None = None, **kwargs: Unpack[ContainerResourceOptions]) -> ContainerResource:
        with check_warnings(self._builder, kwargs, ContainerResourceOptions, "add_container"):
            var_name = valid_var_name(name)
            if tag:
                self._builder.write(f'\nvar {var_name} = builder.AddContainer({format_string(name)}, {format_string(image)}, {format_string(tag)})')
            else:
                self._builder.write(f'\nvar {var_name} = builder.AddContainer({format_string(name)}, {format_string(image)})')
            result = ContainerResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_project(self, name: str, project_path: str, /, *, launch_profile_name: str | None = None, **kwargs: Unpack[ProjectResourceOptions]) -> ProjectResource:
        with check_warnings(self._builder, kwargs, ProjectResourceOptions, "add_project"):
            var_name = valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddProject(name: {format_string(name)}, projectPath: {format_string(project_path)}, launchProfileName: {get_nullable_value(launch_profile_name)})')
            result = ProjectResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_external_service(self, name: str, url: str | ParameterResource, /, **kwargs: Unpack[ResourceOptions]) -> ExternalServiceResource:
        with check_warnings(self._builder, kwargs, ResourceOptions, "add_external_service"):
            var_name = valid_var_name(name)
            if isinstance(url, ParameterResource):
                self._builder.write(f'\nvar {var_name} = builder.AddExternalService({format_string(name)}, {url.name})')
            else:
                self._builder.write(f'\nvar {var_name} = builder.AddExternalService({format_string(name)}, {format_string(url)})')
            result = ExternalServiceResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_csharp_app(self, name: str, path: str, /, **kwargs: Unpack[ProjectResourceOptions]) -> CSharpAppResource:
        with experimental(self._builder, "add_csharp_app", self.__class__, "ASPIRECSHARPAPPS001"):
            with check_warnings(self._builder, kwargs, ProjectResourceOptions, "add_csharp_app"):
                var_name = valid_var_name(name)
                self._builder.write(f'\nvar {var_name} = builder.AddCSharpApp({format_string(name)}, {format_string(path)})')
                result = CSharpAppResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_certificate_authority_collection(self, name: str, /, **kwargs: Unpack[CertificateAuthorityCollectionOptions]) -> CertificateAuthorityCollection:
        with check_warnings(self._builder, kwargs, CertificateAuthorityCollectionOptions, "add_certificate_authority_collection"):
            var_name = valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddCertificateAuthorityCollection({format_string(name)})')
            result = CertificateAuthorityCollection(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_executable(self, name: str, command: str, working_directory: str, /, *, args: Iterable[str] | None = None, **kwargs: Unpack[ExecutableResourceOptions]) -> ExecutableResource:
        with check_warnings(self._builder, kwargs, ExecutableResourceOptions, "add_executable"):
            var_name = valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddExecutable({format_string(name)}, {format_string(command)}, {format_string(working_directory)}, {format_string_array(args)})')
            result = ExecutableResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_dockerfile(self, name: str, context_path: str, /, *, dockerfile_path: str | None = None, stage: str | None = None, **kwargs: Unpack[ContainerResourceOptions]) -> ContainerResource:
        with check_warnings(self._builder, kwargs, ContainerResourceOptions, "add_dockerfile"):
            var_name = valid_var_name(name)
            self._builder.write(f'\nvar {var_name} = builder.AddDockerfile({format_string(name)}, {format_string(context_path)}, {get_nullable_value(dockerfile_path)}, {get_nullable_value(stage)})')
            result = ContainerResource(var_name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result
