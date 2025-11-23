#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithEndpoint(8080, 80, null, "http", null, true, false, null);

builder.Build().Run();
