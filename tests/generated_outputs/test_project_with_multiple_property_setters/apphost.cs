#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var apikey = builder.AddParameter("apikey", "key123", false, false);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null);
myproject.WithReplicas(2);
myproject.WithReplicas(4);
myproject.DisableForwardedHeaders();
myproject.DisableForwardedHeaders();
myproject.WithEnvironment("API_KEY", apikey);
myproject.WithEnvironment("API_KEY", apikey);
myproject.WithReference(db);
myproject.WithHttpEndpoint(8080, null, null, null, true);
myproject.WithHttpEndpoint(8081, null, null, null, true);
myproject.WaitFor(db);
myproject.WaitFor(apikey);
myproject.WithIconName("application");
myproject.WithIconName("application");

builder.Build().Run();
