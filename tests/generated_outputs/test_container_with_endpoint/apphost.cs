#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx")
    .WithEndpoint(port: 8080, targetPort: 80, scheme: null, name: "http", env: null, isProxied: true, isExternal: null, protocol: null);

builder.Build().Run();
