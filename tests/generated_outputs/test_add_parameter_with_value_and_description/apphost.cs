#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "default-value", publishValueAsDefault: false, secret: false)
    .WithDescription(description: "API Key configuration", enableMarkdown: false);

builder.Build().Run();
