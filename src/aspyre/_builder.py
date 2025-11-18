#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from typing import Any, Iterable, Mapping, TypedDict
from typing_extensions import Unpack
import subprocess
import pathlib
import json

from .resources._base import Resource


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


class ResourceBuilder:
    execution_context: Mapping[str, Any]
    environment: Mapping[str, Any]
    resources: Iterable[Resource]
    version: str = "13.0.0"

    def __init__(self, **kwargs: Unpack[DistributedApplicationOptions]) -> None:
        self._options = kwargs
        self.resources = []
        self.execution_context = {}
        self.environment = {}

    def build(self) -> None:
        """Generate csharp project"""
        root_path = pathlib.Path.cwd()
        aspire_dir = root_path / ".aspire"
        if not aspire_dir.exists():
            aspire_dir.mkdir()

        aspyre_dir = aspire_dir / "aspyre"
        if aspyre_dir.exists():
            aspyre_dir.unlink()

        args = [
            "aspire",
            "new",
            "aspire-apphost-singlefile",
            "--version",
            self.version,
            "--name",
            "aspireapp1",
            "--output",
            "./.aspire/aspyre",
            "--non-interactive"
        ]
        output = subprocess.run(args, check=False)
        if output.returncode != 0:
            raise RuntimeError()

        aspire_settings = aspire_dir / "settings.json"
        with aspire_settings.open("w", encoding="utf-8") as f:
            json.dump({"appHostPath": "./.aspire/aspyre/apphost.cs"}, f, indent=4)

        apphost_path = aspyre_dir / "apphost.cs"
        with apphost_path.open("a", encoding="utf-8") as f:
            for resource in self.resources:
                f.write(resource._build())
                f.write("\n")


    def run(self) -> None:
        """Run aspire run command"""


def build_distributed_application(**kwargs: Unpack[DistributedApplicationOptions]) -> ResourceBuilder:
    return ResourceBuilder(**kwargs)
