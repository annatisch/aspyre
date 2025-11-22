
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db", "DATABASE_URL");
var api = builder.AddProject(name: "api", projectPath: "../API/API.csproj", launchProfileName: "Development")
    .WithReplicas(2)
    .WithReference(db)
    .WithHttpEndpoint(5000, null, null, null, true);
var worker = builder.AddProject(name: "worker", projectPath: "../Worker/Worker.csproj", launchProfileName: "Development")
    .WithReference(db)
    .WithReference(api)
    .WaitForStart(api);

builder.Build().Run();
