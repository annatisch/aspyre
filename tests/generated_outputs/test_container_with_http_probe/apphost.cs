#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROBES001
var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx")
    .WithHttpProbe(type: ProbeType.Liveness, path: "/alive", initialDelaySeconds: null, periodSeconds: null, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: (string?)null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
