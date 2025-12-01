#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var nodeapp = builder.AddExecutable(name: "nodeapp", command: "node", workingDirectory: "/app", args: new string[] { "server.js" });

builder.Build().Run();
