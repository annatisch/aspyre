#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from aspyre import build_distributed_application


def test_empty_application():
    builder = build_distributed_application()
    assert builder.build() == """
#:sdk Aspire.AppHost.Sdk

var builder = DistributedApplication.CreateBuilder(args);


builder.Build();
"""

def test_application_with_parameter_resource():
    builder = build_distributed_application()
    password = builder.create_default_password_parameter("password", upper=True, lower=False)
    param_resource = builder.add_resource(password)
    param_resource.exclude_from_manifest = True
    assert builder.build() == """
#:sdk Aspire.AppHost.Sdk

var builder = DistributedApplication.CreateBuilder(args);

var password = builder.CreateDefaultPasswordParameter("password", false, true, true, true, 0, 0, 0, 0);
builder.AddResource(password);
password.ExcludeFromManifest();

builder.Build();
"""

