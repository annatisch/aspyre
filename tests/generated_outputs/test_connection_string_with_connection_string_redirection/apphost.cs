#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var primary = builder.AddConnectionString(name: "primary", environmentVariableName: null);
var secondary = builder.AddConnectionString(name: "secondary", environmentVariableName: null)
    .WithConnectionStringRedirection(resource: primary.Resource);

builder.Build().Run();
