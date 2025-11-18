#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from enum import IntEnum

class IconVariant(IntEnum):
    """Represents the variant of an icon (Regular or Filled)."""

    REGULAR = 0
    """Regular variant of icons."""

    FILLED = 1
    """Filled variant of icons."""