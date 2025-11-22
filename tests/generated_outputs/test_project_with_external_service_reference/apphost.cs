
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var external = builder.AddExternalService("external", "https://api.external.com");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithReference(external)
    .WithHttpEndpoint(5000, null, null, null, true);

builder.Build().Run();
