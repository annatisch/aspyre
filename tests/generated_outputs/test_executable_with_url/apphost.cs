
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithUrl("http://localhost:8080", "My App");

builder.Build().Run();
