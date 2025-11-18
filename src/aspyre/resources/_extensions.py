#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------


from .._builder import ResourceBuilder
from _resources import *

class ExtensionResourceBuilder(ResourceBuilder):

    def add_uvicorn_app(self) -> UvicornApp:
        uvicorn_app = UvicornApp()
        self.resources.append(uvicorn_app)
        return uvicorn_app