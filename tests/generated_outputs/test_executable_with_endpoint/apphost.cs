#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithEndpoint(8080, 80, null, "http", null, true, false, null);

builder.Build().Run();
