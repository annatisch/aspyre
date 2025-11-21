
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService("service1", "http://localhost:8080");
var service2 = builder.AddExternalService("service2", "http://localhost:6379");
service2.WithUrl("http://localhost:6379");
service2.ExcludeFromManifest();
service2.WithHealthCheck("http://localhost:6379/health");
service2.WithReferenceRelationship(service1);
service2.WithIconName("cache", IconVariant.Filled);

builder.Build().Run();
