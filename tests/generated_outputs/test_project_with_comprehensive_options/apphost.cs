#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "secret-key", publishValueAsDefault: false, secret: true);
var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: "Production")
    .WithReplicas(replicas: 3)
    .DisableForwardedHeaders()
    .WithEnvironment(name: "API_KEY", parameter: apikey)
    .WithArgs(args: new string[] { "--verbose" })
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WithHttpEndpoint(port: 5000, targetPort: null, name: "http", env: (string?)null, isProxied: true)
    .WithHttpsEndpoint(port: 5001, targetPort: null, name: "https", env: (string?)null, isProxied: true)
    .WaitFor(dependency: db)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: (string?)null)
    .WithUrl(url: "http://localhost:5000", displayText: (string?)null)
    .WithIconName(iconName: "web", iconVariant: IconVariant.Filled);

builder.Build().Run();
