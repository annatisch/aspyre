#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var config = builder.AddParameter("config", false);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithReferenceRelationship(config)
    .WithIconName("code");

builder.Build().Run();
