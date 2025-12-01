#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExecutable(name: "service1", command: "python", workingDirectory: "/app", args: new string[] { "service1.py" });
var service2 = builder.AddExecutable(name: "service2", command: "python", workingDirectory: "/app", args: new string[] { "service2.py" })
    .WaitForStart(dependency: service1);

builder.Build().Run();
