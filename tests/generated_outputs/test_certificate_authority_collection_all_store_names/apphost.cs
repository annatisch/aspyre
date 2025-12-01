#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var caAddressBook = builder.AddCertificateAuthorityCollection(name: "caAddressBook")
    .WithCertificatesFromStore(storeName: StoreName.AddressBook, storeLocation: StoreLocation.CurrentUser);
var caAuthRoot = builder.AddCertificateAuthorityCollection(name: "caAuthRoot")
    .WithCertificatesFromStore(storeName: StoreName.AuthRoot, storeLocation: StoreLocation.LocalMachine);
var caCertAuthority = builder.AddCertificateAuthorityCollection(name: "caCertAuthority")
    .WithCertificatesFromStore(storeName: StoreName.CertificateAuthority, storeLocation: StoreLocation.CurrentUser);
var caDisallowed = builder.AddCertificateAuthorityCollection(name: "caDisallowed")
    .WithCertificatesFromStore(storeName: StoreName.Disallowed, storeLocation: StoreLocation.LocalMachine);
var caMy = builder.AddCertificateAuthorityCollection(name: "caMy")
    .WithCertificatesFromStore(storeName: StoreName.My, storeLocation: StoreLocation.CurrentUser);
var caRoot = builder.AddCertificateAuthorityCollection(name: "caRoot")
    .WithCertificatesFromStore(storeName: StoreName.Root, storeLocation: StoreLocation.LocalMachine);
var caTrustedPeople = builder.AddCertificateAuthorityCollection(name: "caTrustedPeople")
    .WithCertificatesFromStore(storeName: StoreName.TrustedPeople, storeLocation: StoreLocation.CurrentUser);
var caTrustedPublisher = builder.AddCertificateAuthorityCollection(name: "caTrustedPublisher")
    .WithCertificatesFromStore(storeName: StoreName.TrustedPublisher, storeLocation: StoreLocation.LocalMachine);

builder.Build().Run();
