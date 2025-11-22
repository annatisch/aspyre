#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts")
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"))
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate1.crt"))
    .WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate2.crt"));
var auth = builder.AddContainer("auth", "auth-service")
    .WithHttpEndpoint(8081, null, null, null, true)
    .WithHttpsEndpoint(8444, null, null, null, true);
var api = builder.AddContainer("api", "api-service")
    .WithHttpEndpoint(8080, null, null, null, true)
    .WithHttpsEndpoint(8443, null, null, null, true);

builder.Build().Run();
