#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import os

from aspyre import build_distributed_application
from aspyre.resources._models import IconVariant


def test_resource_with_url_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", url="http://localhost:8080")
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_url_tuple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", url=("http://localhost:8080", "My Service"))
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_exclude_from_mcp(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", exclude_from_mcp=True)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_explicit_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", explicit_start=True)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", health_check="https://localhost:8080/health")
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379", relationship=(service1, "depends-on"))
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379",
                                            relationships=[(service1, "uses"), (service2, "connects-to")])
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_reference_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379", reference_relationship=service1)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_reference_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379",
                                            reference_relationships=[service1, service2])
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_parent_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379", parent_relationship=service1)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_parent_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379",
                                            parent_relationships=[service1, service2])
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_child_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379", child_relationship=service1)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_child_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379",
                                            child_relationships=[service1, service2])
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_icon_name_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", icon_name="web")
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_icon_name_tuple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", icon_name=("database", IconVariant.REGULAR))
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_dockerfile_base_image_true(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080", dockerfile_base_image=True)
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_dockerfile_base_image_dict(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080",
                                           dockerfile_base_image={"build_image": "mcr.microsoft.com/dotnet/sdk:8.0",
                                                                  "runtime_image": "mcr.microsoft.com/dotnet/aspnet:8.0"})
    builder.build(output_dir=export_path)
    verify()


def test_resource_with_multiple_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379",
                                            url="http://localhost:6379",
                                            exclude_from_manifest=True,
                                            health_check="http://localhost:6379/health",
                                            reference_relationship=service1,
                                            icon_name=("cache", IconVariant.FILLED))
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_url_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.url = "http://localhost:8080"
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_url_tuple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.url = ("http://localhost:8080", "My Service")
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.exclude_from_manifest = True
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_exclude_from_mcp(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.exclude_from_mcp = True
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_explicit_start(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.explicit_start = True
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_health_check(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.health_check = "https://localhost:8080/health"
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379")
    service2.relationship = (service1, "depends-on")
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379")
    service3.relationships = [(service1, "uses"), (service2, "connects-to")]
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_reference_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379")
    service2.reference_relationship = service1
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_reference_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379")
    service3.reference_relationships = [service1, service2]
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_parent_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379")
    service2.parent_relationship = service1
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_parent_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379")
    service3.parent_relationships = [service1, service2]
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_child_relationship(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379")
    service2.child_relationship = service1
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_child_relationships(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:5432")
    service3 = builder.add_external_service("service3", "http://localhost:6379")
    service3.child_relationships = [service1, service2]
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_icon_name_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.icon_name = "web"
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_icon_name_tuple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.icon_name = ("database", IconVariant.REGULAR)
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_dockerfile_base_image_true(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.dockerfile_base_image = True
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_dockerfile_base_image_dict(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service = builder.add_external_service("myservice", "http://localhost:8080")
    service.dockerfile_base_image = {"build_image": "mcr.microsoft.com/dotnet/sdk:8.0",
                                     "runtime_image": "mcr.microsoft.com/dotnet/aspnet:8.0"}
    builder.build(output_dir=export_path)
    verify()


def test_resource_property_setters_multiple(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    service1 = builder.add_external_service("service1", "http://localhost:8080")
    service2 = builder.add_external_service("service2", "http://localhost:6379")
    service2.url = "http://localhost:6379"
    service2.exclude_from_manifest = True
    service2.health_check = "http://localhost:6379/health"
    service2.reference_relationship = service1
    service2.icon_name = ("cache", IconVariant.FILLED)
    builder.build(output_dir=export_path)
    verify()

