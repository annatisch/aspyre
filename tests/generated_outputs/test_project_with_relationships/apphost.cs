#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var config = builder.AddParameter(name: "config", secret: false);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithReferenceRelationship(resource: config.Resource)
    .WithIconName(iconName: "code", iconVariant: IconVariant.Filled);

builder.Build().Run();
