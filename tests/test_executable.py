#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application


# Tests for add_executable (basic)
def test_add_executable_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", None)
    builder.build(output_dir=export_path)
    verify()


def test_add_executable_with_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py", "--port", "8080"])
    builder.build(output_dir=export_path)
    verify()


def test_add_executable_node(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("nodeapp", "node", "/app", ["server.js"])
    builder.build(output_dir=export_path)
    verify()


# Tests for ExecutableResource-specific options
def test_executable_with_publish_as_dockerfile(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       ["app.py"],
                                       publish_as_docker_file=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_command(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", None,
                                       command="python3")
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_working_directory(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", None,
                                       working_dir="/app/src")
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions
def test_executable_with_url(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       url=("http://localhost:8080", "My App"))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", [],
                                       exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", [],
                                       icon_name=("terminal", "Regular"))
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEnvironmentOptions
def test_executable_with_environment_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       env=("PORT", "8080"))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_environment_parameter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    port = builder.add_parameter("port", "8080")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       env=("PORT", port))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_reference_connection_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_certificate_trust_scope(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", [],
                                       certificate_trust_scope="Append")
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_developer_certificate_trust(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", None,
                                       developer_certificate_trust=True)
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEndpointsOptions
def test_executable_with_http2_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       as_http2_service=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       endpoint={"port": 8080, "target_port": 80, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_external_http_endpoints(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       external_http_endpoints=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       http_endpoint={"port": 8080, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_https_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       https_endpoint={"port": 8443, "name": "https"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       http_health_check={"path": "/health", "status_code": 200})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_probe(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       http_probe={"type": "Liveness", "path": "/alive"})
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithWaitSupportOptions
def test_executable_with_wait_for(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       wait_for=db)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_behavior(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       wait_for=(db, "StopOnResourceUnavailable"))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_completion(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("config")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       wait_for_completion=param)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_executable("service1", "python", "/app", ["service1.py"])
    service2 = builder.add_executable("service2", "python", "/app", ["service2.py"],
                                     wait_for_start=service1)
    builder.build(output_dir=export_path)
    verify()


# Tests combining multiple options
def test_executable_with_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Dependencies
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # Executable with many options
    executable = builder.add_executable("myapp", "python", "/app",
                                       ["app.py", "--verbose"],
                                       command="python3",
                                       working_dir="/app/src",
                                       publish_as_docker_file=True,
                                       url="http://localhost:8080",
                                       icon_name=("terminal", "Filled"),
                                       env=("API_KEY", api_key),
                                       reference=db,
                                       http_endpoint={"port": 8080, "name": "http"},
                                       https_endpoint={"port": 8443, "name": "https"},
                                       http_health_check={"path": "/health"},
                                       http_probe={"type": "Readiness", "path": "/ready"},
                                       wait_for=db,
                                       certificate_trust_scope="Append")

    builder.build(output_dir=export_path)
    verify()


def test_executable_with_multiple_property_setters(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_connection_string("db")
    api_key = builder.add_external_service("apikey", "https://api.service.com/key")

    executable = builder.add_executable("myapp", "python", "/app", ["app.py"])
    executable.with_command("python3").with_command("python3 -u")
    executable.with_working_dir("/app/src").with_working_dir("/app/src/v2")
    executable.publish_as_docker_file()
    executable.with_env("API_KEY", api_key).with_env("DEBUG", None)
    executable.with_reference(db).with_reference(api_key)
    executable.with_http_endpoint(port=8080, name="http").with_http_endpoint(port=8081, name="http-alt")
    executable.wait_for(db).wait_for(api_key)
    executable.with_icon_name("application").with_icon_name("application", icon_variant="Filled")
    executable.with_http_probe("Liveness", path="/alive").with_http_probe("Readiness", path="/ready")

    builder.build(output_dir=export_path)
    verify()


# Tests with relationships
def test_executable_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    config = builder.add_parameter("config")
    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       reference_relationship=config)

    builder.build(output_dir=export_path)
    verify()


def test_multiple_executables_with_dependencies(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Database
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")
    telemetry = builder.add_connection_string("telemetry", env_var_name="TELEMETRY_URL")

    # API service
    api = builder.add_executable("api", "python", "/app",
                                 ["api.py", "--port", "8000"],
                                 reference=db,
                                 http_endpoint={"port": 8000},
                                 wait_for=db)

    # Worker that depends on API
    worker = builder.add_executable("worker", "python", "/app",
                                    ["worker.py"],
                                    reference=telemetry,
                                    wait_for_start=api)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_external_service_reference(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    external_api = builder.add_external_service("external", "https://api.external.com")

    executable = builder.add_executable("myapp", "python", "/app", ["app.py"],
                                       reference=external_api,
                                       http_endpoint={"port": 8080})

    builder.build(output_dir=export_path)
    verify()


def test_executable_microservices_scenario(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Shared resources
    db_password = builder.add_parameter("dbpassword", "supersecret", secret=True)
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    redis = builder.add_connection_string("redis", env_var_name="REDIS_URL")

    # Gateway service
    gateway = builder.add_executable("gateway", "node", "/app",
                                     ["gateway.js"],
                                     http_endpoint={"port": 8080, "name": "http"},
                                     http_health_check={"path": "/health"},
                                     icon_name=("web", "Filled"))

    # User service
    user_service = builder.add_container("userservice", "python", "/app")

    # Product service
    product_service = builder.add_executable("products", "python", "/app",
                                             ["product_service.py"],
                                             reference=db,
                                             env=("DB_PASSWORD", db_password),
                                             http_endpoint={"port": 8002},
                                             wait_for=db)

    # Order service that depends on both
    order_service = builder.add_executable("orders", "python", "/app",
                                           ["order_service.py"],
                                           reference=redis,
                                           env=("DB_PASSWORD", db_password),
                                           http_endpoint={"port": 8003},
                                           wait_for_start=user_service,
                                           parent_relationship=user_service)

    # Update gateway to reference all services
    gateway.wait_for_start(user_service).wait_for_start(product_service).wait_for_start(order_service)

    builder.build(output_dir=export_path)
    verify()


def test_executable_with_dockerfile_publishing(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_connection_string("db")

    # Python app that should be published as dockerfile
    app = builder.add_executable("pythonapp", "python", "/app",
                                 ["main.py"],
                                 publish_as_docker_file=True,
                                 reference=db,
                                 http_endpoint={"port": 8080},
                                 env=("PORT", "8080"),
                                 dockerfile_base_image={"build_image": "python:3.11",
                                                       "runtime_image": "python:3.11-slim"}).with_env("HOST", "0.0.0.0")

    builder.build(output_dir=export_path)
    verify()
