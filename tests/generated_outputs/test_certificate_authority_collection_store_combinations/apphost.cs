#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var caMy = builder.AddCertificateAuthorityCollection("caMy")
    .WithCertificatesFromStore(StoreName.My, StoreLocation.CurrentUser);
var caRoot = builder.AddCertificateAuthorityCollection("caRoot")
    .WithCertificatesFromStore(StoreName.Root, StoreLocation.LocalMachine);
var caTrusted = builder.AddCertificateAuthorityCollection("caTrusted")
    .WithCertificatesFromStore(StoreName.TrustedPeople, StoreLocation.CurrentUser);

builder.Build().Run();
