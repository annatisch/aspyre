#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var database = builder.AddExternalService(name: "database", url: "postgres://user:pass@dbhost:5432/mydb");
var cache = builder.AddExternalService(name: "cache", url: "redis://cachehost:6379");
var webapp = builder.AddContainer(name: "webapp", image: "myapp")
    .WithReference(externalService: database)
    .WaitForStart(dependency: database);
webapp.WithReference(externalService: cache);
webapp.WaitForStart(dependency: cache);

builder.Build().Run();
