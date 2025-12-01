#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbhost = builder.AddParameterFromConfiguration(name: "dbhost", configurationKey: "ConnectionStrings:DbHost", secret: false)
    .WithDescription(description: "Database host from config", enableMarkdown: false);

builder.Build().Run();
