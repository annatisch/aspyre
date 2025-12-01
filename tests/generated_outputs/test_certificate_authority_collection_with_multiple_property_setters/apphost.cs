#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var cacerts = builder.AddCertificateAuthorityCollection(name: "cacerts");
cacerts.WithCertificate(certificate: X509CertificateLoader.LoadCertificateFromFile("./certs/root-ca.crt"));
cacerts.WithCertificate(certificate: X509CertificateLoader.LoadCertificateFromFile("./certs/extra-ca.crt"));
cacerts.WithCertificatesFromStore(storeName: StoreName.Root, storeLocation: StoreLocation.LocalMachine);
cacerts.WithCertificatesFromStore(storeName: StoreName.My, storeLocation: StoreLocation.CurrentUser);
cacerts.WithCertificatesFromFile(pemFilePath: "./certs/bundle.pem");
cacerts.WithCertificatesFromFile(pemFilePath: "./certs/extra-bundle.pem");

builder.Build().Run();
