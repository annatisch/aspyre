#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application
from aspyre.resources._models import IconVariant, WaitBehavior


# Tests for add_connection_string (basic)
def test_add_connection_string_default(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection")
    builder.build(output_dir=export_path)
    verify()


def test_add_connection_string_with_env_var(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", env_var="MY_CONNECTION_STRING")
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions inherited by ConnectionStringResource
def test_connection_string_with_url_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", url="http://localhost:5432")
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_url_tuple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", url=("http://localhost:5432", "Database Connection"))
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_exclude_from_mcp(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", exclude_from_mcp=True)
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", icon_name=("database", IconVariant.FILLED))
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("myconnection", health_check="https://db.example.com/health")
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithConnectionStringOptions
def test_connection_string_with_connection_string_redirection(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn1 = builder.add_connection_string("primary")
    conn2 = builder.add_connection_string("secondary", connection_string_redirection=conn1)
    builder.build(output_dir=export_path)
    verify()


# Tests combining multiple options
def test_connection_string_with_multiple_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    conn1 = builder.add_connection_string("primary")
    conn2 = builder.add_connection_string("myconnection",
                                        env_var="DB_CONNECTION",
                                        url="http://localhost:5432",
                                        icon_name=("database", IconVariant.REGULAR),
                                        connection_string_redirection=conn1,
                                        health_check="https://db.example.com/health")
    builder.build(output_dir=export_path)
    verify()


# Tests for property setters
def test_connection_string_connection_string_redirection_setter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    conn1 = builder.add_connection_string("primary")
    conn2 = builder.add_connection_string("secondary")
    conn3 = builder.add_connection_string("myconnection")
    conn3.with_connection_string_redirection(conn1).with_connection_string_redirection(conn2)
    conn3.with_url("http://localhost:5432").with_url("http://localhost:5433")
    conn3.with_icon_name("database").with_icon_name(("database2", IconVariant.FILLED))

    builder.build(output_dir=export_path)
    verify()


# Tests with relationships
def test_connection_string_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("dbconfig")
    conn = builder.add_connection_string("myconnection",
                                        reference_relationship=param,
                                        icon_name=("database", IconVariant.FILLED))
    builder.build(output_dir=export_path)
    verify()


def test_connection_string_with_multiple_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param1 = builder.add_parameter("dbhost")
    param2 = builder.add_parameter("dbport")
    service = builder.add_external_service("dbservice", "http://localhost:5432")
    conn = builder.add_connection_string("myconnection",
                                        reference_relationships=[param1, param2],
                                        parent_relationship=service)
    builder.build(output_dir=export_path)
    verify()


# Tests combining with other resources
def test_connection_string_used_by_external_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("dbconnection", env_var="DB_CONNECTION_STRING")
    service = builder.add_external_service("api", "http://localhost:8080",
                                          reference_relationship=conn)
    builder.build(output_dir=export_path)
    verify()


def test_multiple_connection_strings_with_dependencies(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Primary connection string
    primary = builder.add_connection_string("primary",
                                           env_var="PRIMARY_DB",
                                           icon_name=("database", IconVariant.FILLED))

    # Replica connection string that redirects to primary
    replica = builder.add_connection_string("replica",
                                           env_var="REPLICA_DB",
                                           connection_string_redirection=primary)

    # Service that uses replica
    service = builder.add_executable("api", "python", "/app", args=["api.py"],
                                    references=[primary, replica],
                                    wait_for_start=replica)

    builder.build(output_dir=export_path)
    verify()
