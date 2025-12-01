#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var api = builder.AddProject(name: "api", projectPath: "../API/API.csproj", launchProfileName: "Development")
    .WithReplicas(replicas: 2)
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WithHttpEndpoint(port: 5000, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);
var worker = builder.AddProject(name: "worker", projectPath: "../Worker/Worker.csproj", launchProfileName: "Development")
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WaitForStart(dependency: api);

builder.Build().Run();
