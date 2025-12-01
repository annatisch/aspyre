#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "dev-key-123", publishValueAsDefault: false, secret: true);
var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var payments = builder.AddExternalService(name: "payments", url: "https://payments.example.com");
#pragma warning disable ASPIREPROBES001
var api = builder.AddProject(name: "api", projectPath: "../API/API.csproj", launchProfileName: "Development")
    .WithReplicas(replicas: 3)
    .DisableForwardedHeaders()
    .WithArgs(args: new string[] { "--verbose", "--enable-swagger" })
    .WithHttpEndpoint(port: 5000, targetPort: null, name: "http", env: (string?)null, isProxied: true)
    .WithHttpsEndpoint(port: 5001, targetPort: null, name: "https", env: (string?)null, isProxied: true)
    .WaitFor(dependency: db)
    .WithHttpHealthCheck(path: "/health", statusCode: 200, endpointName: (string?)null)
    .WithHttpProbe(type: ProbeType.Liveness, path: "/alive", initialDelaySeconds: null, periodSeconds: null, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: (string?)null)
    .WithUrl(url: "http://localhost:5000", displayText: "API Service")
    .WithHealthCheck(key: "https://localhost:5001/health")
    .WithReferenceRelationship(resource: apikey.Resource)
    .WithIconName(iconName: "web", iconVariant: IconVariant.Filled);
#pragma warning restore ASPIREPROBES001
var worker = builder.AddProject(name: "worker", projectPath: "../Worker/Worker.csproj", launchProfileName: "Development")
    .WithEnvironment(name: "API_KEY", parameter: apikey)
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WaitForStart(dependency: api)
    .WithParentRelationship(parent: api);

builder.Build().Run();
