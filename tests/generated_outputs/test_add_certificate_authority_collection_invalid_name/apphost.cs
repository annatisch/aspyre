#:sdk Aspire.AppHost.Sdk@13.0.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var ca_certs_validname = builder.AddCertificateAuthorityCollection("ca-certs-validname");

builder.Build().Run();
