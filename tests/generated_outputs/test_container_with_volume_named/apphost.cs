#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer(name: "mycontainer", image: "postgres")
    .WithVolume(name: "pgdata", target: "/var/lib/postgresql/data", isReadOnly: false);

builder.Build().Run();
