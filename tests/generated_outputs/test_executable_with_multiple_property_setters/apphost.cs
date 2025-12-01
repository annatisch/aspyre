#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: (string?)null);
var apikey = builder.AddExternalService(name: "apikey", url: "https://api.service.com/key");
var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: new string[] { "app.py" });
myapp.WithCommand(command: "python3");
myapp.WithCommand(command: "python3 -u");
myapp.WithWorkingDirectory(workingDirectory: "/app/src");
myapp.WithWorkingDirectory(workingDirectory: "/app/src/v2");
myapp.PublishAsDockerFile();
myapp.WithEnvironment(name: "API_KEY", externalService: apikey);
myapp.WithEnvironment(name: "DEBUG", value: (string?)null);
myapp.WithReference(source: db, connectionName: (string?)null, optional: false);
myapp.WithReference(externalService: apikey);
myapp.WithHttpEndpoint(port: 8080, targetPort: null, name: "http", env: (string?)null, isProxied: true);
myapp.WithHttpEndpoint(port: 8081, targetPort: null, name: "http-alt", env: (string?)null, isProxied: true);
myapp.WaitFor(dependency: db);
myapp.WaitFor(dependency: apikey);
myapp.WithIconName(iconName: "application", iconVariant: IconVariant.Filled);
myapp.WithIconName(iconName: "application", iconVariant: IconVariant.Filled);
#pragma warning disable ASPIREPROBES001
myapp.WithHttpProbe(type: ProbeType.Liveness, path: "/alive", initialDelaySeconds: null, periodSeconds: null, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: (string?)null);
#pragma warning restore ASPIREPROBES001
#pragma warning disable ASPIREPROBES001
myapp.WithHttpProbe(type: ProbeType.Readiness, path: "/ready", initialDelaySeconds: null, periodSeconds: null, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: (string?)null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
