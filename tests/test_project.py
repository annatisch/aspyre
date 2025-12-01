#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application


# Tests for add_project (basic)
def test_add_project_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj")
    builder.build(output_dir=export_path)
    verify()


def test_add_csharp_app_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_csharp_app("myproject", "../MyProject/MyProject.csproj")
    builder.build(output_dir=export_path)
    verify()


def test_add_project_with_launch_profile(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj", "Development")
    builder.build(output_dir=export_path)
    verify()


# Tests for ProjectResource-specific options
def test_project_with_disable_forwarded_headers(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj", disable_forwarded_headers=True)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_replicas(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj", replicas=3)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_disable_forwarded_headers_and_replicas(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  disable_forwarded_headers=True,
                                  replicas=5)
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions
def test_project_with_url(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  url=("http://localhost:5000", "My Project"))
    builder.build(output_dir=export_path)
    verify()


def test_project_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  icon_name=("code", "Regular"))
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEnvironmentOptions
def test_project_with_environment_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  env=("API_KEY", "test-key-123"))
    builder.build(output_dir=export_path)
    verify()


def test_project_with_environment_parameter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    api_key = builder.add_parameter("apikey", "default-key", secret=True)
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  env=("API_KEY", api_key))
    builder.build(output_dir=export_path)
    verify()


def test_project_with_reference_connection_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    conn = builder.add_connection_string("db", env_var_name="DATABASE_URL")
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  reference=conn)
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithArgsOptions
def test_project_with_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  args=["--verbose", "--port", "5000"])
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithServiceDiscoveryOptions (includes endpoints)
def test_project_with_http2_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  as_http2_service=True)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  endpoint={"port": 8080, "target_port": 80, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_project_with_external_http_endpoints(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  external_http_endpoints=True)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_http_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  http_endpoint={"port": 8080, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_project_with_https_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  https_endpoint={"port": 8443, "name": "https"})
    builder.build(output_dir=export_path)
    verify()


def test_project_with_http_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  http_health_check={"path": "/health", "status_code": 200})
    builder.build(output_dir=export_path)
    verify()


def test_project_with_http_probe(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  http_probe={"type": "Readiness", "path": "/ready", "period_seconds": 10})
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithWaitSupportOptions
def test_project_with_wait_for(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  wait_for=db)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_wait_for_behavior(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  wait_for=(db, "StopOnResourceUnavailable"))
    builder.build(output_dir=export_path)
    verify()


def test_project_with_wait_for_completion(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("config")
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  wait_for_completion=param)
    builder.build(output_dir=export_path)
    verify()


def test_project_with_wait_for_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_executable("myservice", "python", "/app", ["app.py"])
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  wait_for_start=service)
    builder.build(output_dir=export_path)
    verify()


# Tests combining multiple options
def test_project_with_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Create dependencies
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # Create project with many options
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  "Production",
                                  replicas=3,
                                  disable_forwarded_headers=True,
                                  url="http://localhost:5000",
                                  icon_name=("web", "Filled"),
                                  env=("API_KEY", api_key),
                                  reference=db,
                                  args=["--verbose"],
                                  http_endpoint={"port": 5000, "name": "http"},
                                  https_endpoint={"port": 5001, "name": "https"},
                                  http_health_check={"path": "/health"},
                                  wait_for=db)

    builder.build(output_dir=export_path)
    verify()


def test_project_with_multiple_property_setters(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_connection_string("db")
    api_key = builder.add_parameter("apikey", "key123")

    project = builder.add_project("myproject", "../MyProject/MyProject.csproj")
    project.with_replicas(2).with_replicas(4)
    project.disable_forwarded_headers().disable_forwarded_headers()
    project.with_env("API_KEY", api_key).with_env("API_KEY", None)
    project.with_http_endpoint(port=8080).with_http_endpoint(port=8081)
    project.wait_for(db).wait_for(api_key)
    project.with_icon_name("application").with_icon_name("application")

    builder.build(output_dir=export_path)
    verify()


# Tests with relationships
def test_project_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    config = builder.add_parameter("config")
    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  reference_relationship=config,
                                  icon_name="code")

    builder.build(output_dir=export_path)
    verify()


def test_multiple_projects_with_dependencies(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Shared database
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # API project
    api = builder.add_project("api", "../API/API.csproj",
                             "Development",
                             reference=db,
                             http_endpoint={"port": 5000},
                             replicas=2)

    # Worker project that depends on API
    worker = builder.add_project("worker", "../Worker/Worker.csproj",
                                "Development",
                                reference=db,
                                wait_for_start=api)

    builder.build(output_dir=export_path)
    verify()


def test_project_with_external_service_reference(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    external_api = builder.add_external_service("external", "https://api.external.com")

    project = builder.add_project("myproject", "../MyProject/MyProject.csproj",
                                  reference=external_api,
                                  http_endpoint={"port": 5000})

    builder.build(output_dir=export_path)
    verify()


def test_project_full_scenario(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Parameters
    api_key = builder.add_parameter("apikey", "dev-key-123", secret=True)

    # Database connection
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # External service
    payment_service = builder.add_external_service("payments", "https://payments.example.com")

    # Main API project
    api = builder.add_project("api", "../API/API.csproj",
                             "Development",
                             replicas=3,
                             disable_forwarded_headers=True,
                             url=("http://localhost:5000", "API Service"),
                             icon_name=("web", "Filled"),
                             args=["--verbose", "--enable-swagger"],
                             http_endpoint={"port": 5000, "name": "http"},
                             https_endpoint={"port": 5001, "name": "https"},
                             http_health_check={"path": "/health", "status_code": 200},
                             http_probe={"type": "Liveness", "path": "/alive"},
                             wait_for=db,
                             reference_relationship=api_key,
                             health_check="https://localhost:5001/health")

    # Background worker
    worker = builder.add_project("worker", "../Worker/Worker.csproj",
                                "Development",
                                reference=db,
                                env=("API_KEY", api_key),
                                wait_for_start=api,
                                parent_relationship=api)

    builder.build(output_dir=export_path)
    verify()
