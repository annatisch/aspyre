#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithEndpoint(port: 8080, targetPort: 80, scheme: (string?)null, name: "http", env: (string?)null, isProxied: true, isExternal: null, protocol: null);

builder.Build().Run();
