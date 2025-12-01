#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbconnection = builder.AddConnectionString(name: "dbconnection", environmentVariableName: "DB_CONNECTION_STRING");
var api = builder.AddExternalService(name: "api", url: "http://localhost:8080")
    .WithReferenceRelationship(resourceBuilder: dbconnection);

builder.Build().Run();
