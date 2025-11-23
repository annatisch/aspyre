#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WaitFor(db);

builder.Build().Run();
