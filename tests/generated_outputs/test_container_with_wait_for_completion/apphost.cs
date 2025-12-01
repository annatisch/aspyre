#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var config = builder.AddParameter(name: "config", secret: false);
var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WaitForCompletion(dependency: config, exitCode: 0);

builder.Build().Run();
