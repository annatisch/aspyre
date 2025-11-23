#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""Comprehensive tests for CertificateAuthorityCollection class."""

import pytest

from aspyre import build_distributed_application
from aspyre.resources._models import (
    StoreName,
    StoreLocation,
    IconVariant,
)


# Tests for add_certificate_authority_collection (basic)
def test_add_certificate_authority_collection_basic(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts")
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificate_string(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificate="./certs/ca.crt")
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificate_bytes(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    cert_data = b"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t"  # Mock base64 cert data
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificate=cert_data)
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_strings(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates=["./certs/ca1.crt", "./certs/ca2.crt"])
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_bytes(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    cert1 = b"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0xLS0tLQ=="
    cert2 = b"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0yLS0tLQ=="
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates=[cert1, cert2])
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_mixed(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    cert_bytes = b"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0xLS0tLQ=="
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates=[cert_bytes, "./certs/ca2.crt"])
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_store_my(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.MY, StoreLocation.CURRENT_USER))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_store_root(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.ROOT, StoreLocation.LOCAL_MACHINE))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_store_auth_root(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.AUTH_ROOT, StoreLocation.LOCAL_MACHINE))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_store_ca(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.CERTIFICATE_AUTHORITY, StoreLocation.CURRENT_USER))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_store_trusted_people(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.TRUSTED_PEOPLE, StoreLocation.CURRENT_USER))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_certificates_from_file(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_file="./certs/bundle.pem")
    builder.build(output_dir=export_path)
    verify()


# Tests for ResourceOptions
def test_add_certificate_authority_collection_with_url(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 url=("https://ca.example.com", "CA Management"))
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_exclude_from_manifest(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 exclude_from_manifest=True)
    builder.build(output_dir=export_path)
    verify()


def test_add_certificate_authority_collection_with_icon_name(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 icon_name=("certificate", IconVariant.FILLED))
    builder.build(output_dir=export_path)
    verify()


# Tests for combining multiple options
def test_certificate_authority_collection_with_multiple_sources(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificate="./certs/root-ca.crt",
                                                                 certificates=["./certs/intermediate1.crt", "./certs/intermediate2.crt"],
                                                                 certificates_from_file="./certs/trusted-bundle.pem")
    builder.build(output_dir=export_path)
    verify()


def test_certificate_authority_collection_with_comprehensive_options(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates=["./certs/ca1.crt", "./certs/ca2.crt"],
                                                                 certificates_from_store=(StoreName.ROOT, StoreLocation.LOCAL_MACHINE),
                                                                 url="https://ca.example.com",
                                                                 icon_name=("shield", IconVariant.FILLED))
    builder.build(output_dir=export_path)
    verify()


def test_certificate_authority_collection_with_multiple_property_setters(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts")
    ca_collection.with_certificate("./certs/root-ca.crt").with_certificate("./certs/extra-ca.crt")
    ca_collection.with_certificates_from_store(StoreName.ROOT, StoreLocation.LOCAL_MACHINE).with_certificates_from_store(StoreName.MY, StoreLocation.CURRENT_USER)
    ca_collection.with_certificates_from_file("./certs/bundle.pem").with_certificates_from_file("./certs/extra-bundle.pem")
    builder.build(output_dir=export_path)
    verify()


# Tests with containers using the certificate collection
def test_certificate_authority_collection_with_container_reference(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()
    ca_collection = builder.add_certificate_authority_collection("cacerts",
                                                                 certificates_from_store=(StoreName.ROOT, StoreLocation.LOCAL_MACHINE))
    container = builder.add_container("webapp", "nginx",
                                     reference=ca_collection)
    builder.build(output_dir=export_path)
    verify()


def test_certificate_authority_collection_in_microservices_scenario(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Certificate authority collection
    ca_certs = builder.add_certificate_authority_collection("cacerts",
                                                            certificate="./certs/root-ca.crt",
                                                            certificates=["./certs/intermediate1.crt", "./certs/intermediate2.crt"])

    # Services that need the CA certificates
    auth_service = builder.add_container("auth", "auth-service",
                                        reference=ca_certs,
                                        http_endpoint={"port": 8081},
                                        https_endpoint={"port": 8444})

    api_service = builder.add_container("api", "api-service",
                                       references=[ca_certs],
                                       http_endpoint={"port": 8080},
                                       https_endpoint={"port": 8443})

    builder.build(output_dir=export_path)
    verify()


# Tests for different store names and locations combinations
def test_certificate_authority_collection_store_combinations(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    # Different store combinations
    ca1 = builder.add_certificate_authority_collection("caMy",
                                                       certificates_from_store=(StoreName.MY, StoreLocation.CURRENT_USER))
    ca2 = builder.add_certificate_authority_collection("caRoot",
                                                       certificates_from_store=(StoreName.ROOT, StoreLocation.LOCAL_MACHINE))
    ca3 = builder.add_certificate_authority_collection("caTrusted",
                                                       certificates_from_store=(StoreName.TRUSTED_PEOPLE, StoreLocation.CURRENT_USER))

    builder.build(output_dir=export_path)
    verify()


# Test with all store name enums
def test_certificate_authority_collection_all_store_names(verify_dotnet_apphost):
    export_path, verify = verify_dotnet_apphost
    builder = build_distributed_application()

    ca_address_book = builder.add_certificate_authority_collection("caAddressBook",
                                                                   certificates_from_store=(StoreName.ADDRESS_BOOK, StoreLocation.CURRENT_USER))
    ca_auth_root = builder.add_certificate_authority_collection("caAuthRoot",
                                                                certificates_from_store=(StoreName.AUTH_ROOT, StoreLocation.LOCAL_MACHINE))
    ca_cert_authority = builder.add_certificate_authority_collection("caCertAuthority",
                                                                     certificates_from_store=(StoreName.CERTIFICATE_AUTHORITY, StoreLocation.CURRENT_USER))
    ca_disallowed = builder.add_certificate_authority_collection("caDisallowed",
                                                                certificates_from_store=(StoreName.DISALLOWED, StoreLocation.LOCAL_MACHINE))
    ca_my = builder.add_certificate_authority_collection("caMy",
                                                         certificates_from_store=(StoreName.MY, StoreLocation.CURRENT_USER))
    ca_root = builder.add_certificate_authority_collection("caRoot",
                                                           certificates_from_store=(StoreName.ROOT, StoreLocation.LOCAL_MACHINE))
    ca_trusted_people = builder.add_certificate_authority_collection("caTrustedPeople",
                                                                     certificates_from_store=(StoreName.TRUSTED_PEOPLE, StoreLocation.CURRENT_USER))
    ca_trusted_publisher = builder.add_certificate_authority_collection("caTrustedPublisher",
                                                                        certificates_from_store=(StoreName.TRUSTED_PUBLISHER, StoreLocation.LOCAL_MACHINE))

    builder.build(output_dir=export_path)
    verify()
