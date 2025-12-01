#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREDOCKERFILEBUILDER001
var myservice = builder.AddExternalService(name: "myservice", url: "http://localhost:8080")
    .WithDockerfileBaseImage();
#pragma warning restore ASPIREDOCKERFILEBUILDER001

builder.Build().Run();
