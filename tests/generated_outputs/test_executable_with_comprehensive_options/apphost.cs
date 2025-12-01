#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "secret-key", publishValueAsDefault: false, secret: true);
var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
#pragma warning disable ASPIREPROBES001
var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: new string[] { "app.py", "--verbose" })
    .PublishAsDockerFile()
    .WithCommand(command: "python3")
    .WithWorkingDirectory(workingDirectory: "/app/src")
    .WithEnvironment(name: "API_KEY", parameter: apikey)
    .WithReference(source: db, connectionName: null, optional: false)
    .WithHttpEndpoint(port: 8080, targetPort: null, name: "http", env: null, isProxied: true)
    .WithHttpsEndpoint(port: 8443, targetPort: null, name: "https", env: null, isProxied: true)
    .WaitFor(dependency: db)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: null)
    .WithCertificateTrustScope(scope: CertificateTrustScope.Append)
    .WithHttpProbe(type: ProbeType.Readiness, path: "/ready", initialDelaySeconds: null, periodSeconds: null, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: null)
    .WithUrl(url: "http://localhost:8080", displayText: null)
    .WithIconName(iconName: "terminal", iconVariant: IconVariant.Filled);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
