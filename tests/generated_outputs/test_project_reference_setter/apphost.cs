
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null);
myproject.WithReference(db);

builder.Build().Run();
