#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var version = builder.AddParameter(name: "version", value: "1.0.0", publishValueAsDefault: false, secret: false);
var myapp = builder.AddDockerfile(name: "myapp", contextPath: "./app", dockerfilePath: null, stage: null)
    .WithBuildArg(name: "VERSION", value: version);

builder.Build().Run();
