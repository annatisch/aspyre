#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: "Development");

builder.Build().Run();
