#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var config1 = builder.AddParameter(name: "config1", secret: false);
var config2 = builder.AddParameter(name: "config2", secret: false)
    .WithReferenceRelationship(resourceBuilder: config1);

builder.Build().Run();
