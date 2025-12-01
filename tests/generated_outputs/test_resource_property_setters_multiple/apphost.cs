#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService(name: "service1", url: "http://localhost:8080");
var service2 = builder.AddExternalService(name: "service2", url: "http://localhost:6379");
var service3 = builder.AddExternalService(name: "service3", url: "http://localhost:5432");
service3.WithUrl(url: "http://localhost:6379", displayText: (string?)null);
service3.WithUrl(url: "http://localhost:6379", displayText: "Cache Service");
service3.ExcludeFromManifest();
service3.ExcludeFromManifest();
service3.WithHealthCheck(key: "http://localhost:6379/health");
service3.WithHealthCheck(key: "http://localhost:6379/health");
service3.WithReferenceRelationship(resource: service1.Resource);
service3.WithReferenceRelationship(resource: service2.Resource);
service3.WithChildRelationship(child: service1);
service3.WithChildRelationship(child: service2);
service3.WithIconName(iconName: "cache", iconVariant: IconVariant.Filled);
service3.WithIconName(iconName: "cache", iconVariant: IconVariant.Filled);
service3.WithParentRelationship(parent: service1);
service3.WithParentRelationship(parent: service2);
service3.WithRelationship(resource: service1.Resource, type: "uses");
service3.WithRelationship(resource: service2.Resource, type: "connects-to");
service3.ExcludeFromMcp();
service3.ExcludeFromMcp();
service3.WithExplicitStart();
service3.WithExplicitStart();
#pragma warning disable ASPIREDOCKERFILEBUILDER001
service3.WithDockerfileBaseImage(buildImage: "mcr.microsoft.com/dotnet/sdk:8.0", runtimeImage: (string?)null);
#pragma warning restore ASPIREDOCKERFILEBUILDER001
#pragma warning disable ASPIREDOCKERFILEBUILDER001
service3.WithDockerfileBaseImage(buildImage: (string?)null, runtimeImage: "mcr.microsoft.com/dotnet/sdk:8.0");
#pragma warning restore ASPIREDOCKERFILEBUILDER001
#pragma warning disable ASPIREDOCKERFILEBUILDER001
service3.WithDockerfileBaseImage(buildImage: (string?)null, runtimeImage: (string?)null);
#pragma warning restore ASPIREDOCKERFILEBUILDER001

builder.Build().Run();
