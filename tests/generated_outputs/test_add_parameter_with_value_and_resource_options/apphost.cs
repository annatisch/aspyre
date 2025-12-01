#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "secret-value", publishValueAsDefault: true, secret: true)
    .WithDescription(description: "API Key", enableMarkdown: false)
    .ExcludeFromManifest()
    .WithIconName(iconName: "key", iconVariant: IconVariant.Regular);

builder.Build().Run();
