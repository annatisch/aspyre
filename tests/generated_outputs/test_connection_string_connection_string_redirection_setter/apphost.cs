#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService(name: "myservice", url: "http://localhost:8080");
var primary = builder.AddConnectionString(name: "primary", environmentVariableName: (string?)null);
var secondary = builder.AddConnectionString(name: "secondary", environmentVariableName: (string?)null);
var myconnection = builder.AddConnectionString(name: "myconnection", environmentVariableName: (string?)null);
myconnection.WithConnectionStringRedirection(resource: primary.Resource);
myconnection.WithConnectionStringRedirection(resource: secondary.Resource);
myconnection.WithUrl(url: "http://localhost:5432", displayText: (string?)null);
myconnection.WithUrl(url: "http://localhost:5433", displayText: (string?)null);
myconnection.WithIconName(iconName: "database", iconVariant: IconVariant.Filled);
myconnection.WithIconName(iconName: "database", iconVariant: IconVariant.Filled);

builder.Build().Run();
