#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from ._base import (
    Resource,
    ConnectionStringResource,
    ConnectionStringResourceOptions,
    ParameterResource,
    ParameterResourceOptions,
    ProjectResource,
    ProjectResourceOptions,
    ExecutableResource,
    ExecutableResourceOptions,
    ContainerResource,
    ContainerResourceOptions,
)
from ._models import (
    IconVariant,
    WaitBehavior,
    ProtocolType,
    ProbeType,
    ContainerLifetime,
    ImagePullPolicy,
    UnixFileMode,

)

try:
    from aspyre_extensions.resources import __all__ as _extension_resources
    from aspyre_extensions.resources import *
except ImportError:
    _extension_resources = []

__all__ = [
    "Resource",
    "ConnectionStringResource",
    "ConnectionStringResourceOptions",
    "ParameterResource",
    "ParameterResourceOptions",
    "ProjectResource",
    "ProjectResourceOptions",
    "ExecutableResource",
    "ExecutableResourceOptions",
    "ContainerResource",
    "ContainerResourceOptions",
    "IconVariant",
    "WaitBehavior",
    "ProtocolType",
    "ProbeType",
    "ContainerLifetime",
    "ImagePullPolicy",
    "UnixFileMode",
]

__all__.extend([e for e in _extension_resources if e not in __all__])  # pyright: ignore
