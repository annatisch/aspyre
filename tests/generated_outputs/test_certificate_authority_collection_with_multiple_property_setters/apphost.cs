#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection("cacerts");
cacerts.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"));
cacerts.WithCertificate(X509CertificateLoader.LoadCertificateFromFile("./certs/extra-ca.crt"));
cacerts.WithCertificatesFromStore(StoreName.Root, StoreLocation.LocalMachine);
cacerts.WithCertificatesFromStore(StoreName.My, StoreLocation.CurrentUser);
cacerts.WithCertificatesFromFile("./certs/bundle.pem");
cacerts.WithCertificatesFromFile("./certs/extra-bundle.pem");

builder.Build().Run();
