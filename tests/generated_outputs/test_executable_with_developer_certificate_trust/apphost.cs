#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: null)
    .WithDeveloperCertificateTrust(trust: true);

builder.Build().Run();
