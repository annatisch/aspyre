#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WithDockerfile(contextPath: "Dockerfile.production", dockerfilePath: null, stage: null);

builder.Build().Run();
