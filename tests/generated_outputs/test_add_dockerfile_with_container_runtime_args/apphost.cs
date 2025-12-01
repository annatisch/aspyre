#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile(name: "myapp", contextPath: "./app", dockerfilePath: null, stage: null)
    .WithContainerRuntimeArgs(args: new string[] { "--cpus", "2", "--memory", "1g" });

builder.Build().Run();
