#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db", "DATABASE_URL");
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithReference(db);

builder.Build().Run();
