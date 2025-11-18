#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from typing import Literal
from ._base import Resource

class UvicornApp(Resource):
    @property
    def package(self) -> Literal["Aspire.Hosting.Python"]:
        return "Aspire.Hosting.Python"

    def __init__(self) -> None:
        super().__init__()
