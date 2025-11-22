#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts")
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"))
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate1.crt"))
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate2.crt"))
    .WithCertificatesFromFile("./certs/trusted-bundle.pem");

builder.Build().Run();
