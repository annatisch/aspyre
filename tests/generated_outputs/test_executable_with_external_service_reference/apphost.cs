#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var external = builder.AddExternalService(name: "external", url: "https://api.external.com");
var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: new string[] { "app.py" })
    .WithReference(externalService: external)
    .WithHttpEndpoint(port: 8080, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);

builder.Build().Run();
