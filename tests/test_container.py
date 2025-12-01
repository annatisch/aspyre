#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""Comprehensive tests for ContainerResource class."""

import pytest

from aspyre import build_distributed_application


# Tests for add_container (basic)
def test_add_container_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx")
    builder.build(output_dir=export_path)
    verify()


def test_add_container_with_tag(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx", "1.25")
    builder.build(output_dir=export_path)
    verify()


def test_add_container_with_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx", args=["-g", "daemon off;"])
    builder.build(output_dir=export_path)
    verify()


# Tests for add_dockerfile (basic)
def test_add_dockerfile_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_dockerfile_path(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app", dockerfile_path="Dockerfile.production")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_stage(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app", stage="production")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_dockerfile_path_and_stage(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       dockerfile_path="docker/Dockerfile.multi",
                                       stage="release")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app", args=["--verbose", "--debug"])
    builder.build(output_dir=export_path)
    verify()


# Tests for add_dockerfile with ContainerResource-specific options
def test_add_dockerfile_with_publish_as_container(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app", publish_as_container=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_bind_mount(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       bind_mount=("/host/path", "/container/path"))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_bind_mount_readonly(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       bind_mount=("/host/path", "/container/path"))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_build_arg(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    version = builder.add_parameter("version", "1.0.0")
    container = builder.add_dockerfile("myapp", "./app",
                                       build_arg=("VERSION", version))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_build_secret(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    container = builder.add_dockerfile("myapp", "./app",
                                       build_secret=("API_KEY", api_key))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_container_runtime_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       container_runtime_args=["--cpus", "2", "--memory", "1g"])
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_container_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       container_name="my-app-container")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_entrypoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       entrypoint="/app/entrypoint.sh")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_image_pull_policy(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       image_pull_policy="Always")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_image_registry(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       image_registry="myregistry.azurecr.io")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_lifetime_session(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       lifetime="Session")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_lifetime_persistent(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       lifetime="Persistent")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_volume_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       volume="/app/data")
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_volume_named(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       volume={"name": "appdata", "target": "/app/data"})
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_volume_readonly(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       volume={"target": "/app/config", "name": "config", "is_read_only": True})
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_environment_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       env=("PORT", "8080"))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_environment_parameter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    port = builder.add_parameter("port", "8080")
    container = builder.add_dockerfile("myapp", "./app",
                                       env=("PORT", port))
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_reference_connection_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")
    container = builder.add_dockerfile("myapp", "./app",
                                       reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_multiple_references(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    container = builder.add_dockerfile("myapp", "./app",
                                       reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_http_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       http_endpoint={"port": 8080, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_https_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       https_endpoint={"port": 8443, "name": "https"})
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_http_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_dockerfile("myapp", "./app",
                                       http_health_check={"path": "/health", "status_code": 200})
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_wait_for(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    container = builder.add_dockerfile("myapp", "./app",
                                       wait_for=db)
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_with_wait_for_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_container("service1", "postgres")
    service2 = builder.add_dockerfile("myapp", "./app",
                                      wait_for_start=service1)
    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Dependencies
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    version = builder.add_parameter("version", "1.0.0")
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # Dockerfile container with many options
    container = builder.add_dockerfile("myapp", "./app",
                                       dockerfile_path="docker/Dockerfile.production",
                                       stage="release",
                                       args=["--verbose"],
                                       publish_as_container=True,
                                       bind_mount=("/host/data", "/app/data"),
                                       build_arg=("VERSION", version),
                                       build_secret=("API_KEY", api_key),
                                       container_name="my-app-container",
                                       entrypoint="/app/start.sh",
                                       image_pull_policy="Always",
                                       lifetime="Persistent",
                                       volume={"name": "appdata", "target": "/app/data"},
                                       url="http://localhost:8080",
                                       icon_name=("box", "Filled"),
                                       env=("DEBUG", "true"),
                                       reference=db,
                                       http_endpoint={"port": 8080, "name": "http"},
                                       https_endpoint={"port": 8443, "name": "https"},
                                       http_health_check={"path": "/health"},
                                       wait_for=db)

    builder.build(output_dir=export_path)
    verify()


def test_add_dockerfile_microservices_scenario(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Infrastructure
    postgres = builder.add_container("postgres", "postgres", "16",
                                    env=("POSTGRES_PASSWORD", "dev-password"),
                                    volume={"name": "pgdata", "target": "/var/lib/postgresql/data"},
                                    lifetime="Persistent",
                                    http_endpoint={"port": 5432})

    redis = builder.add_container("redis", "redis", "7-alpine",
                                 lifetime="Persistent",
                                 http_endpoint={"port": 6379})

    # Services built from Dockerfiles
    auth_service = builder.add_dockerfile("auth", "./services/auth",
                                         dockerfile_path="Dockerfile",
                                         stage="production",
                                         exclude_from_manifest=True,
                                         wait_for_start=postgres,
                                         http_endpoint={"port": 8081},
                                         http_health_check={"path": "/health"})

    api_service = builder.add_dockerfile("api", "./services/api",
                                        dockerfile_path="Dockerfile.multi",
                                        stage="release",
                                        wait_for_start=postgres,
                                        http_endpoint={"port": 8080},
                                        https_endpoint={"port": 8443},
                                        http_health_check={"path": "/health"})

    builder.build(output_dir=export_path)
    verify()


# Tests for ContainerResource-specific options
def test_container_with_publish_as_container(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx", publish_as_container=True)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_bind_mount(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     bind_mount=("/host/path", "/container/path"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_bind_mount_readonly(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     bind_mount=("/host/path", "/container/path"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_build_arg(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    version = builder.add_parameter("version", "1.0.0")
    container = builder.add_container("mycontainer", "myapp",
                                     build_arg=("VERSION", version))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_build_secret(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    container = builder.add_container("mycontainer", "myapp",
                                     build_secret=("API_KEY", api_key))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_container_runtime_args(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     container_runtime_args=["--cpus", "2", "--memory", "1g"])
    builder.build(output_dir=export_path)
    verify()


def test_container_with_container_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     container_name="my-nginx-container")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_dockerfile(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                     dockerfile="Dockerfile.production")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_dockerfile_and_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                     dockerfile={
                                         "context_path":"Dockerfile.multi",
                                         "dockerfile_path": "docker/Dockerfile",
                                         "stage": "production"
                                     })
    builder.build(output_dir=export_path)
    verify()


def test_container_with_endpoint_proxy_support(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     endpoint_proxy_support=True)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_entrypoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                     entrypoint="/app/entrypoint.sh")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_setter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image="nginx:alpine")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_and_tag(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image=("nginx", "1.25-alpine"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_pull_policy(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image_pull_policy="Always")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_registry_custom(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image_registry="myregistry.azurecr.io")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_sha256(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image_sha256="abc123def456")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_image_tag(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     image_tag="1.25-alpine")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_lifetime_session(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     lifetime="Session")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_lifetime_persistent(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "postgres",
                                     lifetime="Persistent")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_volume_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "postgres",
                                     volume="/var/lib/postgresql/data")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_volume_named(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "postgres",
                                     volume=("pgdata", "/var/lib/postgresql/data"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_volume_readonly(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     volume={"target": "/usr/share/nginx/html", "name": "html", "is_read_only": True})
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions
def test_container_with_url(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     url=("http://localhost:8080", "Web UI"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     icon_name=("box", "Filled"))
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEnvironmentOptions
def test_container_with_environment_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     env=("PORT", "8080"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_environment_parameter(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    port = builder.add_parameter("port", "8080")
    container = builder.add_container("mycontainer", "nginx",
                                     env=("PORT", port))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_reference_connection_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")
    container = builder.add_container("mycontainer", "myapp",
                                     reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_multiple_references(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    container = builder.add_container("mycontainer", "myapp",
                                     reference=db)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_certificate_trust_scope(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                     certificate_trust_scope="Append")
    builder.build(output_dir=export_path)
    verify()


def test_container_with_developer_certificate_trust(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                     developer_certificate_trust=True)
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithEndpointsOptions
def test_container_with_http2_service(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "myapp",
                                      as_http2_service=True)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     endpoint={"port": 8080, "target_port": 80, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_container_with_external_http_endpoints(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     external_http_endpoints=True)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_http_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     http_endpoint={"port": 8080, "name": "http"})
    builder.build(output_dir=export_path)
    verify()


def test_container_with_https_endpoint(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     https_endpoint={"port": 8443, "name": "https"})
    builder.build(output_dir=export_path)
    verify()


def test_container_with_http_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     http_health_check={"path": "/health", "status_code": 200})
    builder.build(output_dir=export_path)
    verify()


def test_container_with_http_probe(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    container = builder.add_container("mycontainer", "nginx",
                                     http_probe={"type": "Liveness", "path": "/alive"})
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceWithWaitSupportOptions
def test_container_with_wait_for(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    container = builder.add_container("mycontainer", "myapp",
                                     wait_for=db)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_wait_for_behavior(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    container = builder.add_container("mycontainer", "myapp",
                                     wait_for=(db, "StopOnResourceUnavailable"))
    builder.build(output_dir=export_path)
    verify()


def test_container_with_wait_for_completion(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    param = builder.add_parameter("config")
    container = builder.add_container("mycontainer", "myapp",
                                     wait_for_completion=param)
    builder.build(output_dir=export_path)
    verify()


def test_container_with_wait_for_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_container("service1", "postgres")
    service2 = builder.add_container("service2", "myapp",
                                    wait_for_start=service1)
    builder.build(output_dir=export_path)
    verify()


# Tests for property setters
def test_container_with_multiple_property_setters(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    db = builder.add_connection_string("db")
    cache = builder.add_connection_string("cache")
    container = builder.add_container("mycontainer", "nginx")
    container.publish_as_container().publish_as_container()
    container.with_bind_mount("/host/path", "/container/path").with_bind_mount("/host/path", "/container/path", is_read_only=True)
    container.with_container_name("my-nginx-container").with_container_name("another-name")
    container.with_entrypoint("/app/entrypoint.sh").with_entrypoint("/app/another-entrypoint.sh")
    container.with_image("nginx:alpine").with_image("nginx", tag="latest")
    container.with_env("PORT", "8080").with_env("PORT", "9090")
    container.with_reference(db, connection_name="db", optional=True).with_reference(cache)
    container.with_http_endpoint(
        port=8080,
        name="http",
        target_port=80,
        env="env",
        is_proxied=False,
    ).with_http_endpoint(
        port=9090,
        name="http-alt"
    )
    container.wait_for(db).wait_for(cache)
    builder.build(output_dir=export_path)
    container.with_volume("pgdata", "/var/lib/postgresql/data", is_read_only=False).with_volume("/var/lib/postgresql/data")
    container.with_lifetime("Persistent").with_lifetime("Session")
    verify()


# Tests combining multiple options
def test_container_with_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Dependencies
    api_key = builder.add_parameter("apikey", "secret-key", secret=True)
    db = builder.add_connection_string("db", env_var_name="DATABASE_URL")

    # Container with many options
    container = builder.add_container("mycontainer", "myapp", "1.0.0",
                                     args=["--verbose"],
                                     publish_as_container=True,
                                     bind_mount={"source": "/host/data", "target": "/app/data", "is_read_only": True},
                                     container_name="my-app-container",
                                     entrypoint="/app/start.sh",
                                     image_pull_policy="Always",
                                     lifetime="Persistent",
                                     volume={"name": "appdata", "target": "/app/data"},
                                     url="http://localhost:8080",
                                     icon_name=("box", "Filled"),
                                     env=("API_KEY", api_key),
                                     reference=db,
                                     http_endpoint={"port": 8080, "name": "http"},
                                     https_endpoint={"port": 8443, "name": "https"},
                                     http_health_check={"path": "/health"},
                                     http_probe={"type": "Readiness", "path": "/ready"},
                                     wait_for=db,
                                     certificate_trust_scope="Append").with_env("DEBUG", "true")

    builder.build(output_dir=export_path)
    verify()


# Tests with relationships
def test_container_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    db = builder.add_external_service("database", "postgres://user:pass@dbhost:5432/mydb")
    cache = builder.add_external_service("cache", "redis://cachehost:6379")
    app = builder.add_container("webapp", "myapp",
                                reference=db,
                                wait_for_start=db).with_reference(cache).wait_for_start(cache)

    builder.build(output_dir=export_path)
    verify()


def test_multiple_containers_with_dependencies(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Database
    postgres = builder.add_container("postgres", "postgres", "16",
                                    env=("POSTGRES_PASSWORD", "password"),
                                    volume={"name": "pgdata", "target": "/var/lib/postgresql/data"},
                                    lifetime="Persistent",
                                    http_endpoint={"port": 5432})

    # Cache
    redis = builder.add_container("redis", "redis", "7",
                                 lifetime="Persistent",
                                 http_endpoint={"port": 6379})

    # Application
    app = builder.add_container("webapp", "myapp",
                               wait_for_start=postgres,
                               http_endpoint={"port": 8080},
                               https_endpoint={"port": 8443},
                               http_health_check={"path": "/health"}).wait_for_start(redis)

    builder.build(output_dir=export_path)
    verify()


def test_container_with_external_service_reference(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    external_api = builder.add_external_service("api", "https://api.example.com")
    container = builder.add_container("mycontainer", "myapp",
                                     reference=external_api)

    builder.build(output_dir=export_path)
    verify()


def test_container_with_dockerfile_build(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    version = builder.add_parameter("version", "1.0.0")
    api_key = builder.add_parameter("buildkey", "secret", secret=True)

    container = builder.add_container("mycontainer", "myapp",
                                     dockerfile="Dockerfile",
                                     build_arg=("VERSION", version),
                                     build_secret=("BUILD_KEY", api_key))

    builder.build(output_dir=export_path)
    verify()
