#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithHttpsEndpoint(8443, null, "https", null, true);

builder.Build().Run();
