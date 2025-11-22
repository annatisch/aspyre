
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: "Production")
    .DisableForwardedHeaders()
    .WithReplicas(3)
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("ENV", "production")
    .WithReference(db)
    .WithArgs(new string[] { "--verbose" })
    .WithHttpEndpoint(5000, null, "http", null, true)
    .WithHttpsEndpoint(5001, null, "https", null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WaitFor(db)
    .WithUrl("http://localhost:5000")
    .WithIconName("web", IconVariant.Filled);

builder.Build().Run();
