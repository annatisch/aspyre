#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts")
    .WithCertificates(certificates: new List<X509Certificate2> { X509CertificateLoader.LoadCertificateFromFile("./certs/ca1.crt"), X509CertificateLoader.LoadCertificateFromFile("./certs/ca2.crt") });

builder.Build().Run();
