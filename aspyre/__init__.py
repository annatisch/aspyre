#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

import sys
import pathlib

from ._version import VERSION

_cwd = pathlib.Path.cwd()
sys.path.insert(0, str(_cwd / ".aspire"))


try:
    from aspire_extensions import DistributedApplicationBuilder as ExtendedDistributedApplicationBuilder

    def build_distributed_application(*args) -> ExtendedDistributedApplicationBuilder:
        return ExtendedDistributedApplicationBuilder(*args)

except ImportError:
    from ._builder import _DistributedApplicationBuilder as DistributedApplicationBuilder

    def build_distributed_application(*args) -> DistributedApplicationBuilder:
        return DistributedApplicationBuilder(*args)


__version__ = VERSION
__all__ = [
    "build_distributed_application",
]
