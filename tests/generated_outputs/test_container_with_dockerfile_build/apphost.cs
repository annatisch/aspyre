#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var version = builder.AddParameter(name: "version", value: "1.0.0", publishValueAsDefault: false, secret: false);
var buildkey = builder.AddParameter(name: "buildkey", value: "secret", publishValueAsDefault: false, secret: true);
var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WithDockerfile(contextPath: "Dockerfile", dockerfilePath: (string?)null, stage: (string?)null)
    .WithBuildArg(name: "VERSION", value: version)
    .WithBuildSecret(name: "BUILD_KEY", value: buildkey);

builder.Build().Run();
