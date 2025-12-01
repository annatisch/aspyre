#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROXYENDPOINTS001
var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx")
    .WithEndpointProxySupport(proxyEnabled: true);
#pragma warning restore ASPIREPROXYENDPOINTS001

builder.Build().Run();
