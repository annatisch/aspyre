#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "secret-key", publishValueAsDefault: false, secret: true);
var myapp = builder.AddDockerfile(name: "myapp", contextPath: "./app", dockerfilePath: null, stage: null)
    .WithBuildSecret(name: "API_KEY", value: apikey);

builder.Build().Run();
