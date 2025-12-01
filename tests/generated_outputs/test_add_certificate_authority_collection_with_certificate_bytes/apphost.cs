#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts")
    .WithCertificate(certificate: X509CertificateLoader.LoadCertificate(Convert.FromBase64String("TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHRMUzB0")));

builder.Build().Run();
