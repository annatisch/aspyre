#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts")
    .WithCertificates(certificates: new List<X509Certificate2> { X509CertificateLoader.LoadCertificate(Convert.FromBase64String("TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHhMUzB0TFE9PQ==")), X509CertificateLoader.LoadCertificate(Convert.FromBase64String("TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHlMUzB0TFE9PQ==")) });

builder.Build().Run();
