#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var external = builder.AddExternalService(name: "external", url: "https://api.external.com");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithReference(externalService: external)
    .WithHttpEndpoint(port: 5000, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);

builder.Build().Run();
