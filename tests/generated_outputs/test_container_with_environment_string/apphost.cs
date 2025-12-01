#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx")
    .WithEnvironment(name: "PORT", value: "8080");

builder.Build().Run();
