#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class Annotations:
    experimental: str | None
    deprecated: str | None

