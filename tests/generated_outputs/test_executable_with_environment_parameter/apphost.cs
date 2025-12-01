#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var port = builder.AddParameter(name: "port", value: "8080", publishValueAsDefault: false, secret: false);
var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: new string[] { "app.py" })
    .WithEnvironment(name: "PORT", parameter: port);

builder.Build().Run();
