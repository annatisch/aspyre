#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithArgs(args: new string[] { "--verbose", "--port", "5000" });

builder.Build().Run();
