
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db1 = builder.AddConnectionString("db1");
var db2 = builder.AddConnectionString("db2");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithReference(db1)
    .WithReference(db2);

builder.Build().Run();
