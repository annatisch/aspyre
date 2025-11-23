#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithEnvironment("API_KEY", "test-key-123");

builder.Build().Run();
