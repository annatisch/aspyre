#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var caMy = builder.AddCertificateAuthorityCollection(name: "caMy")
    .WithCertificatesFromStore(storeName: StoreName.My, storeLocation: StoreLocation.CurrentUser);
var caRoot = builder.AddCertificateAuthorityCollection(name: "caRoot")
    .WithCertificatesFromStore(storeName: StoreName.Root, storeLocation: StoreLocation.LocalMachine);
var caTrusted = builder.AddCertificateAuthorityCollection(name: "caTrusted")
    .WithCertificatesFromStore(storeName: StoreName.TrustedPeople, storeLocation: StoreLocation.CurrentUser);

builder.Build().Run();
