#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts")
    .WithCertificate(X509CertificateLoader.LoadCertificate(Convert.FromBase64String("TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHhMUzB0TFE9PQ==")))
    .WithCertificate(X509CertificateLoader.LoadCertificate(Convert.FromBase64String("TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHlMUzB0TFE9PQ==")));

builder.Build().Run();
