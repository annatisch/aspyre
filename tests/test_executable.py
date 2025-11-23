#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application
from aspyre.resources._models import IconVariant, WaitBehavior, ProbeType, ProtocolType, CertificateTrustScope


# Tests for add_executable (basic)
def test_add_executable_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app")
    builder.build(output_dir=export_path)
    verify()


def test_add_executable_with_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py", "--port", "8080"])
    builder.build(output_dir=export_path)
    verify()


def test_add_executable_node(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("nodeapp", "node", "/app", args=["server.js"])
    builder.build(output_dir=export_path)
    verify()


# Tests for ExecutableResource-specific options
def test_executable_with_publish_as_dockerfile(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       args=["app.py"],
                                       publish_as_dockerfile=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_command(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       command="python3")
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_working_directory(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       working_directory="/app/src")
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions
def test_executable_with_url(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       url=("http://localhost:8080", "My App"))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       icon_name=("terminal", IconVariant.REGULAR))
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEnvironmentOptions
def test_executable_with_environment_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       environment=("PORT", "8080"))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_environment_parameter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    port = builder.add_parameter("port", "8080")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       environment=("PORT", port))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_multiple_environments(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    api_key = builder.add_parameter("apikey", "key123", secret=True)
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       environments=[("API_KEY", api_key), ("DEBUG", "true")])
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_reference_connection_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db", env_var="DATABASE_URL")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_multiple_references(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    cache = builder.add_connection_string("cache")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       references=[db, cache])
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_certificate_trust_scope(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       certificate_trust_scope=CertificateTrustScope.APPEND)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_developer_certificate_trust(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app",
                                       developer_certificate_trust=True)
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEndpointsOptions
def test_executable_with_http2_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       http2_service=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       endpoint={"port": 8080, "target_port": 80, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_external_http_endpoints(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       external_http_endpoints=True)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       http_endpoint={"port": 8080, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_https_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       https_endpoint={"port": 8443, "name": "https"})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       http_health_check={"path": "/health", "status_code": 200})
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_http_probe(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       http_probe={"type": ProbeType.LIVENESS, "path": "/alive"})
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithWaitSupportOptions
def test_executable_with_wait_for(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       wait_for=db)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_behavior(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       wait_for=(db, WaitBehavior.STOP_ON_RESOURCE_UNAVAILABLE))
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_completion(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("config")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       wait_for_completion=param)
    builder.build(output_dir=export_path)
    verify()


def test_executable_with_wait_for_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_executable("service1", "python", "/app", args=["service1.py"])
    service2 = builder.add_executable("service2", "python", "/app", args=["service2.py"],
                                     wait_for_start=service1)
    builder.build(output_dir=export_path)
    verify()


# Tests combining multiple options
def test_executable_with_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Dependencies
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    db = builder.add_connection_string("db", env_var="DATABASE_URL")

    # Executable with many options
    executable = builder.add_executable("myapp", "python", "/app",
                                       args=["app.py", "--verbose"],
                                       command="python3",
                                       working_directory="/app/src",
                                       publish_as_dockerfile=True,
                                       url="http://localhost:8080",
                                       icon_name=("terminal", IconVariant.FILLED),
                                       environments=[("API_KEY", api_key), ("DEBUG", "true")],
                                       reference=db,
                                       http_endpoint={"port": 8080, "name": "http"},
                                       https_endpoint={"port": 8443, "name": "https"},
                                       http_health_check={"path": "/health"},
                                       http_probe={"type": ProbeType.READINESS, "path": "/ready"},
                                       wait_for=db,
                                       certificate_trust_scope=CertificateTrustScope.APPEND)

    builder.build(output_dir=export_path)
    verify()


def test_executable_with_multiple_property_setters(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_connection_string("db")
    api_key = builder.add_parameter("apikey", "key123")

    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"])
    executable.with_command("python3").with_command("python3 -u")
    executable.with_working_directory("/app/src").with_working_directory("/app/src/v2")
    executable.publish_as_dockerfile()
    executable.with_environment(("API_KEY", api_key)).with_environment(("DEBUG", "true"))
    executable.with_reference(db).with_reference(api_key)
    executable.with_http_endpoint(port=8080, name="http").with_http_endpoint(port=8081, name="http-alt")
    executable.wait_for(db).wait_for(api_key)
    executable.with_icon_name("application").with_icon_name(("application", IconVariant.FILLED))
    executable.with_http_probe(type=ProbeType.LIVENESS, path="/alive").with_http_probe(type=ProbeType.READINESS, path="/ready")

    builder.build(output_dir=export_path)
    verify()


# Tests with relationships
def test_executable_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    config = builder.add_parameter("config")
    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       reference_relationship=config)

    builder.build(output_dir=export_path)
    verify()


def test_multiple_executables_with_dependencies(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Database
    db = builder.add_connection_string("db", env_var="DATABASE_URL")

    # API service
    api = builder.add_executable("api", "python", "/app",
                                 args=["api.py", "--port", "8000"],
                                 reference=db,
                                 http_endpoint={"port": 8000},
                                 wait_for=db)

    # Worker that depends on API
    worker = builder.add_executable("worker", "python", "/app",
                                    args=["worker.py"],
                                    references=[db, api],
                                    wait_for_start=api)

    builder.build(output_dir=export_path)
    verify()


def test_executable_with_external_service_reference(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    external_api = builder.add_external_service("external", "https://api.external.com")

    executable = builder.add_executable("myapp", "python", "/app", args=["app.py"],
                                       reference=external_api,
                                       http_endpoint={"port": 8080})

    builder.build(output_dir=export_path)
    verify()


def test_executable_microservices_scenario(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Shared resources
    db_password = builder.add_parameter("dbpassword", "supersecret", secret=True)
    db = builder.add_connection_string("db", env_var="DATABASE_URL")

    redis = builder.add_connection_string("redis", env_var="REDIS_URL")

    # Gateway service
    gateway = builder.add_executable("gateway", "node", "/app",
                                     args=["gateway.js"],
                                     http_endpoint={"port": 8080, "name": "http"},
                                     http_health_check={"path": "/health"},
                                     icon_name=("web", IconVariant.FILLED))

    # User service
    user_service = builder.add_executable("users", "python", "/app",
                                          args=["user_service.py"],
                                          references=[db, redis],
                                          environments=[("DB_PASSWORD", db_password)],
                                          http_endpoint={"port": 8001},
                                          http_probe={"type": ProbeType.LIVENESS, "path": "/alive"},
                                          wait_for=db)

    # Product service
    product_service = builder.add_executable("products", "python", "/app",
                                             args=["product_service.py"],
                                             reference=db,
                                             environment=("DB_PASSWORD", db_password),
                                             http_endpoint={"port": 8002},
                                             wait_for=db)

    # Order service that depends on both
    order_service = builder.add_executable("orders", "python", "/app",
                                           args=["order_service.py"],
                                           references=[db, user_service, product_service],
                                           environment=("DB_PASSWORD", db_password),
                                           http_endpoint={"port": 8003},
                                           wait_for_start=[user_service, product_service],
                                           parent_relationships=[user_service, product_service])

    # Update gateway to reference all services
    gateway.with_reference(user_service).with_reference(product_service).with_reference(order_service)
    gateway.wait_for_start(user_service).wait_for_start(product_service).wait_for_start(order_service)

    builder.build(output_dir=export_path)
    verify()


def test_executable_with_dockerfile_publishing(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_connection_string("db")

    # Python app that should be published as dockerfile
    app = builder.add_executable("pythonapp", "python", "/app",
                                 args=["main.py"],
                                 publish_as_dockerfile=True,
                                 reference=db,
                                 http_endpoint={"port": 8080},
                                 environments=[
                                     ("PORT", "8080"),
                                     ("HOST", "0.0.0.0")
                                 ],
                                 dockerfile_base_image={"build_image": "python:3.11",
                                                       "runtime_image": "python:3.11-slim"})

    builder.build(output_dir=export_path)
    verify()
