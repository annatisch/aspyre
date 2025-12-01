#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "default-key", publishValueAsDefault: false, secret: true);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WithEnvironment(name: "API_KEY", parameter: apikey);

builder.Build().Run();
