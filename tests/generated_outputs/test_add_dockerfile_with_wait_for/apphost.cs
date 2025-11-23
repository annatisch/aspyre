#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WaitFor(db);

builder.Build().Run();
