#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: null);
var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WaitFor(dependency: db);

builder.Build().Run();
