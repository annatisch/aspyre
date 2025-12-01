#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService(name: "service1", url: "http://localhost:8080");
var service2 = builder.AddExternalService(name: "service2", url: "http://localhost:6379")
    .WithUrl(url: "http://localhost:6379", displayText: (string?)null)
    .ExcludeFromManifest()
    .WithHealthCheck(key: "http://localhost:6379/health")
    .WithReferenceRelationship(resource: service1.Resource)
    .WithIconName(iconName: "cache", iconVariant: IconVariant.Filled);

builder.Build().Run();
