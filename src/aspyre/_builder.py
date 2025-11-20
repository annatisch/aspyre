#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from typing import Any, Iterable, Mapping, TypedDict, overload
from typing_extensions import Unpack
import subprocess
import pathlib
import json

from .resources._base import (
    Resource,
    ResourceOptions,
    ResourceWithConnectionString,
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


class DistributedApplicationBuilder:
    version: str = "13.0.0"

    def __init__(self, *args) -> None:
        self._dependencies = []
        self._builder = "var builder = DistributedApplication.CreateBuilder(args);\n"

    def build(self) -> None:
        dependencies = set(self._dependencies)
        self._builder = "\n".join([f"{d}@{self.version}" for d in dependencies]) + "\n" + self._builder
        self._builder += "\nbuilder.Build().Run();\n"

    def add_resource(self, resource: Resource, **kwargs: Unpack[ResourceOptions]) -> Resource:
        self._builder += f"\nbuilder.AddResource({resource.name})"
        return Resource(resource.name, builder=self._builder, **kwargs)

    @overload
    def add_parameter(self, name: str, /,*, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]):
        ...
    @overload
    def add_parameter(
        self,
        name: str,
        /, *,
        value: str,
        publish_value_as_default: bool = False,
        secret: bool = False,
        **kwargs: Unpack[ParameterResourceOptions]
    ) -> ParameterResource:
        ...
    def add_parameter(self, *args, **kwargs):
        name = args[0]
        secret = kwargs.pop("secret", False)
        value = kwargs.pop("value", None)
        publish_value_as_default = kwargs.pop("publish_value_as_default", False)
        if not value:
            self._builder += f'\nvar {name} = builder.AddParameter("{name}", {str(secret).lower()})'
        else:
            self._builder += f'\nvar {name} = builder.AddParameter("{name}", "{value}", {str(publish_value_as_default).lower()}, {str(secret).lower()})'
        result = ParameterResource(name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_parameter_from_configuration(self, name: str, *, configuration_key: str, secret: bool = False, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        self._builder += f'\nvar {name} = builder.AddParameterFromConfiguration("{name}",  "{configuration_key}", {str(secret).lower()});'
        result = ParameterResource(name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_connection_string(self, name: str, /, *, environment_variable_name: str | None = None, **kwargs: Unpack[ParameterResourceOptions]) -> ResourceWithConnectionString:
        if environment_variable_name:
            self._builder += f'\nvar {name} = builder.AddConnectionString("{name}", "{environment_variable_name}");'
        else:
            self._builder += f'\nvar {name} = builder.AddConnectionString("{name}");'
        return ResourceWithConnectionString()
        #TODO: return resource, fix kwargs
        #public static ApplicationModel.IResourceBuilder<ApplicationModel.IResourceWithConnectionString> AddConnectionString(this IDistributedApplicationBuilder builder, string name, string? environmentVariableName = null) { throw null; }

    def create_default_password_parameter(self, name: str, /, *, lower: bool = True, upper: bool = True, numeric: bool = True, special: bool = True, min_lower: int = 0, min_upper: int = 0, min_numeric: int = 0, min_special: int = 0, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        self._builder += f'\nvar {name} = builder.CreateDefaultPasswordParameter("{name}", {str(lower).lower()}, {str(upper).lower()}, {str(numeric).lower()}, {str(special).lower()}, {min_lower}, {min_upper}, {min_numeric}, {min_special})'
        result = ParameterResource(name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def create_parameter(self, name: str, /, *, secret: bool, **kwargs: Unpack[ParameterResourceOptions]) -> ParameterResource:
        self._builder += f'\nvar {name} = builder.CreateParameter("{name}", {str(secret).lower()});'
        result = ParameterResource(name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result

    def add_project(self, name: str, /, *, project_path: str | None = None, launch_profile_name: str | None = None, **kwargs: Unpack[ProjectResourceOptions]) -> ProjectResource:
        self._builder += f'\nvar {name} = builder.AddProject("{name}"'
        if project_path:
            self._builder += f', "{project_path}"'
        if launch_profile_name:
            self._builder += f', "{launch_profile_name}"'
        self._builder += ')'
        result = ProjectResource(name, builder=self._builder, **kwargs)
        self._dependencies.append(result.package)
        return result




def build_distributed_application(*args) -> DistributedApplicationBuilder:
    return DistributedApplicationBuilder(*args)
