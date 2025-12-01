#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExecutable(name: "myservice", command: "python", workingDirectory: "/app", args: new string[] { "app.py" });
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj")
    .WaitForStart(dependency: myservice);

builder.Build().Run();
