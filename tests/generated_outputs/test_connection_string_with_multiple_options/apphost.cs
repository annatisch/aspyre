#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService(name: "myservice", url: "http://localhost:8080");
var primary = builder.AddConnectionString(name: "primary", environmentVariableName: (string?)null);
var myconnection = builder.AddConnectionString(name: "myconnection", environmentVariableName: "DB_CONNECTION")
    .WithConnectionStringRedirection(resource: primary.Resource)
    .WithUrl(url: "http://localhost:5432", displayText: (string?)null)
    .WithHealthCheck(key: "https://db.example.com/health")
    .WithIconName(iconName: "database", iconVariant: IconVariant.Regular);

builder.Build().Run();
