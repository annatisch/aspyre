#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROBES001
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithHttpProbe(type: ProbeType.Readiness, path: "/ready", initialDelaySeconds: null, periodSeconds: 10, timeoutSeconds: null, failureThreshold: null, successThreshold: null, endpointName: (string?)null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
