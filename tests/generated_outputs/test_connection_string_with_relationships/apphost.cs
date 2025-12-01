#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbconfig = builder.AddParameter(name: "dbconfig", secret: false);
var myconnection = builder.AddConnectionString(name: "myconnection", environmentVariableName: null)
    .WithReferenceRelationship(resourceBuilder: dbconfig)
    .WithIconName(iconName: "database", iconVariant: IconVariant.Filled);

builder.Build().Run();
