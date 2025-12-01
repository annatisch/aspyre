#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", secret: true)
    .WithDescription(description: "API Key for service", enableMarkdown: false)
    .WithIconName(iconName: "security", iconVariant: IconVariant.Filled)
    .ExcludeFromMcp();

builder.Build().Run();
