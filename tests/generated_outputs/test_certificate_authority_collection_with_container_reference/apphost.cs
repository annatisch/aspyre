#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts")
    .WithCertificatesFromStore(StoreName.Root, StoreLocation.LocalMachine);
var webapp = builder.AddContainer("webapp", "nginx");

builder.Build().Run();
