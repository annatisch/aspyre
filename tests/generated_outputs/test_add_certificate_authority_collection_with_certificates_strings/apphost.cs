#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts")
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/ca1.crt"))
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/ca2.crt"));

builder.Build().Run();
