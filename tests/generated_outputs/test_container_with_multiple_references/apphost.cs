
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var cache = builder.AddConnectionString("cache");
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithReference(db)
    .WithReference(cache);

builder.Build().Run();
