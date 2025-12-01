#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts")
    .WithCertificate(certificate: X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"))
    .WithCertificates(certificates: new List<X509Certificate2> { X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate1.crt"), X509CertificateLoader.LoadCertificateFromFile("./certs/intermediate2.crt") })
    .WithCertificatesFromFile(pemFilePath: "./certs/trusted-bundle.pem");

builder.Build().Run();
