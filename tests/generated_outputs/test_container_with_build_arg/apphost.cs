#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var version = builder.AddParameter(name: "version", value: "1.0.0", publishValueAsDefault: false, secret: false);
var mycontainer = builder.AddContainer(name: "mycontainer", image: "myapp")
    .WithBuildArg(name: "VERSION", value: version);

builder.Build().Run();
