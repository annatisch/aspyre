#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts");
cacerts.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/ca1.crt"));
cacerts.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/ca2.crt"));
cacerts.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/ca3.crt"));

builder.Build().Run();
