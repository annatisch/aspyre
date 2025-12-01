#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var telemetry = builder.AddConnectionString(name: "telemetry", environmentVariableName: "TELEMETRY_URL");
var api = builder.AddExecutable(name: "api", command: "python", workingDirectory: "/app", args: new string[] { "api.py", "--port", "8000" })
    .WithReference(source: db, connectionName: null, optional: false)
    .WithHttpEndpoint(port: 8000, targetPort: null, name: null, env: null, isProxied: true)
    .WaitFor(dependency: db);
var worker = builder.AddExecutable(name: "worker", command: "python", workingDirectory: "/app", args: new string[] { "worker.py" })
    .WithReference(source: telemetry, connectionName: null, optional: false)
    .WaitForStart(dependency: api);

builder.Build().Run();
