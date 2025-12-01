#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbhost = builder.AddParameter(name: "dbhost", secret: false);
var dbservice = builder.AddExternalService(name: "dbservice", url: "http://localhost:5432");
var myconnection = builder.AddConnectionString(name: "myconnection", environmentVariableName: null)
    .WithReferenceRelationship(resourceBuilder: dbhost)
    .WithParentRelationship(parent: dbservice);

builder.Build().Run();
