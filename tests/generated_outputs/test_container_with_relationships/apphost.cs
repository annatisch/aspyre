#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var database = builder.AddExternalService("database", "postgres://user:pass@dbhost:5432/mydb");
var cache = builder.AddExternalService("cache", "redis://cachehost:6379");
var webapp = builder.AddContainer("webapp", "myapp")
    .WithReference(database)
    .WithReference(cache)
    .WaitForStart(database)
    .WaitForStart(cache);

builder.Build().Run();
