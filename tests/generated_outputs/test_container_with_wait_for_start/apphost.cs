#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddContainer(name: "service1", image: "postgres");
var service2 = builder.AddContainer(name: "service2", image: "myapp")
    .WaitForStart(dependency: service1);

builder.Build().Run();
