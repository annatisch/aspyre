#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var api = builder.AddExternalService(name: "api", url: "https://api.example.com");
var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WithReference(externalService: api);

builder.Build().Run();
