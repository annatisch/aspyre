#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx")
    .WithVolume(name: "html", target: "/usr/share/nginx/html", isReadOnly: true);

builder.Build().Run();
