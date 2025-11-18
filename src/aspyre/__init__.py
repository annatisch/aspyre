#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
from ._version import VERSION
from ._builder import build_distributed_application, ResourceBuilder

__version__ = VERSION
__all__ = [
    "build_distributed_application",
    "ResourceBuilder",
]
