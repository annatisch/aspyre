#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "default-key", false, true);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithEnvironment("API_KEY", apikey);

builder.Build().Run();
