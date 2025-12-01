#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: (string?)null);
#pragma warning disable ASPIREDOCKERFILEBUILDER001
var pythonapp = builder.AddExecutable(name: "pythonapp", command: "python", workingDirectory: "/app", args: new string[] { "main.py" })
    .PublishAsDockerFile()
    .WithEnvironment(name: "PORT", value: "8080")
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WithHttpEndpoint(port: 8080, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true)
    .WithDockerfileBaseImage(buildImage: "python:3.11", runtimeImage: "python:3.11-slim");
#pragma warning restore ASPIREDOCKERFILEBUILDER001
pythonapp.WithEnvironment(name: "HOST", value: "0.0.0.0");

builder.Build().Run();
