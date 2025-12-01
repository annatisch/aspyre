#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application


# Tests for add_parameter (no value)
def test_add_parameter_no_value_default(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_no_value_secret(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", secret=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_no_value_with_description(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", description="API Key for service")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_no_value_with_resource_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey",
                                  secret=True,
                                  description="API Key for service",
                                  exclude_from_mcp=True,
                                  icon_name="security")
    builder.build(output_dir=export_path)
    verify()


# Tests for add_parameter (with value)
def test_add_parameter_with_value_default(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "default-key-value")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_with_value_secret(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "secret-key-value", secret=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_with_value_publish_as_default(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "default-key", publish_value_as_default=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_with_value_all_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "secret-value",
                                  publish_value_as_default=True,
                                  secret=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_with_value_and_description(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "default-value",
                                  description="API Key configuration")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_with_value_and_resource_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("apikey", "secret-value",
                                  secret=True,
                                  publish_value_as_default=True,
                                  description=("API Key", False),
                                  icon_name=("key", "Regular"),
                                  exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


# Tests for add_parameter_from_configuration
def test_add_parameter_from_configuration_default(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter_from_config("dbhost", "ConnectionStrings:DbHost")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_from_configuration_secret(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter_from_config("dbpassword", "ConnectionStrings:DbPassword", secret=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_from_configuration_with_description(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter_from_config("dbhost", "ConnectionStrings:DbHost",
                                                     description="Database host from config")
    builder.build(output_dir=export_path)
    verify()


def test_add_parameter_from_configuration_with_resource_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter_from_config("dbpassword", "ConnectionStrings:DbPassword",
                                                     secret=True,
                                                     description=("Database password from configuration", True),
                                                     icon_name="database",
                                                     health_check="https://db.example.com/health")
    builder.build(output_dir=export_path)
    verify()


# Tests for description property setter
def test_parameter_description_setter_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("myconfig")
    param.with_description("Configuration value").with_description("Configuration value v2", enable_markdown=False)
    builder.build(output_dir=export_path)
    verify()


# Tests combining parameters with other resources
def test_parameter_used_in_external_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    url_param = builder.add_parameter("serviceurl", "http://localhost:8080")
    service = builder.add_external_service("myservice", url_param)
    builder.build(output_dir=export_path)
    verify()


def test_parameter_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param1 = builder.add_parameter("config1")
    param2 = builder.add_parameter("config2", reference_relationship=param1)
    builder.build(output_dir=export_path)
    verify()
