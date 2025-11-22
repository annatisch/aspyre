#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var caAddressBook = builder.AddCertificateAuthorityCollection("caAddressBook")
    .WithCertificatesFromStore(StoreName.AddressBook, StoreLocation.CurrentUser);
var caAuthRoot = builder.AddCertificateAuthorityCollection("caAuthRoot")
    .WithCertificatesFromStore(StoreName.AuthRoot, StoreLocation.LocalMachine);
var caCertAuthority = builder.AddCertificateAuthorityCollection("caCertAuthority")
    .WithCertificatesFromStore(StoreName.CertificateAuthority, StoreLocation.CurrentUser);
var caDisallowed = builder.AddCertificateAuthorityCollection("caDisallowed")
    .WithCertificatesFromStore(StoreName.Disallowed, StoreLocation.LocalMachine);
var caMy = builder.AddCertificateAuthorityCollection("caMy")
    .WithCertificatesFromStore(StoreName.My, StoreLocation.CurrentUser);
var caRoot = builder.AddCertificateAuthorityCollection("caRoot")
    .WithCertificatesFromStore(StoreName.Root, StoreLocation.LocalMachine);
var caTrustedPeople = builder.AddCertificateAuthorityCollection("caTrustedPeople")
    .WithCertificatesFromStore(StoreName.TrustedPeople, StoreLocation.CurrentUser);
var caTrustedPublisher = builder.AddCertificateAuthorityCollection("caTrustedPublisher")
    .WithCertificatesFromStore(StoreName.TrustedPublisher, StoreLocation.LocalMachine);

builder.Build().Run();
