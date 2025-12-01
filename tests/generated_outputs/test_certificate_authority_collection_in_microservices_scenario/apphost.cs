#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts")
    .WithCertificate(certificate: X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"))
    .WithCertificates(certificates: new List<X509Certificate2> { X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate1.crt"), X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate2.crt") });
var auth = builder.AddContainer(name: "auth", image: "auth-service")
    .WithHttpEndpoint(port: 8081, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true)
    .WithHttpsEndpoint(port: 8444, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);
auth.WithCertificateAuthorityCollection(certificateAuthorityCollection: cacerts);
auth.WithDeveloperCertificateTrust(trust: false);
var api = builder.AddContainer(name: "api", image: "api-service")
    .WithHttpEndpoint(port: 8080, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true)
    .WithHttpsEndpoint(port: 8443, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);
api.WithCertificateAuthorityCollection(certificateAuthorityCollection: cacerts);
api.WithDeveloperCertificateTrust(trust: true);

builder.Build().Run();
