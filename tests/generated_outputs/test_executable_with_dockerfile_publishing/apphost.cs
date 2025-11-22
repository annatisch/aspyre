
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var pythonapp = builder.AddExecutable("pythonapp", "python", "/app", new string[] { "main.py" })
    .PublishAsDockerFile()
    .WithEnvironment("PORT", "8080")
    .WithEnvironment("HOST", "0.0.0.0")
    .WithReference(db)
    .WithHttpEndpoint(8080, null, null, null, true)
    .WithDockerfileBaseImage("python:3.11", "python:3.11-slim");

builder.Build().Run();
