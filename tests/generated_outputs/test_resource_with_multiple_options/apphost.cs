
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService("service1", "http://localhost:8080");
var service2 = builder.AddExternalService("service2", "http://localhost:6379")
    .WithUrl("http://localhost:6379")
    .ExcludeFromManifest()
    .WithHealthCheck("http://localhost:6379/health")
    .WithReferenceRelationship(service1)
    .WithIconName("cache", IconVariant.Filled);

builder.Build().Run();
