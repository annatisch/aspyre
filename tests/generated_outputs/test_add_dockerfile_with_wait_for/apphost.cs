#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: null);
var myapp = builder.AddDockerfile(name: "myapp", contextPath: "./app", dockerfilePath: null, stage: null)
    .WaitFor(dependency: db);

builder.Build().Run();
