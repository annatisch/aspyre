#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService("service1", "http://localhost:8080");
var service2 = builder.AddExternalService("service2", "http://localhost:6379");
var service3 = builder.AddExternalService("service3", "http://localhost:5432");
service3.WithUrl("http://localhost:6379");
service3.WithUrl("http://localhost:6379", "Cache Service");
service3.ExcludeFromManifest();
service3.ExcludeFromManifest();
service3.WithHealthCheck("http://localhost:6379/health");
service3.WithHealthCheck("http://localhost:6379/health");
service3.WithReferenceRelationship(service1);
service3.WithReferenceRelationship(service2);
service3.WithChildRelationship(service1);
service3.WithChildRelationship(service2);
service3.WithIconName("cache", IconVariant.Filled);
service3.WithParentRelationship(service1);
service3.WithParentRelationship(service2);
service3.WithRelationship(service1.Resource, "uses");
service3.WithRelationship(service2.Resource, "connects-to");
service3.ExcludeFromMcp();
service3.ExcludeFromMcp();
service3.WithExplicitStart();
service3.WithExplicitStart();
service3.WithDockerfileBaseImage("mcr.microsoft.com/dotnet/sdk:8.0", null);
service3.WithDockerfileBaseImage(null, "mcr.microsoft.com/dotnet/sdk:8.0");
service3.WithDockerfileBaseImage();

builder.Build().Run();
