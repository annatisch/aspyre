#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbpassword = builder.AddParameterFromConfiguration(name: "dbpassword", configurationKey: "ConnectionStrings:DbPassword", secret: true)
    .WithDescription(description: "Database password from configuration", enableMarkdown: true)
    .WithHealthCheck(key: "https://db.example.com/health")
    .WithIconName(iconName: "database", iconVariant: IconVariant.Filled);

builder.Build().Run();
