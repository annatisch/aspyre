
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "dev-key-123", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var payments = builder.AddExternalService("payments", "https://payments.example.com");
var api = builder.AddProject(name: "api", projectPath: "../API/API.csproj", launchProfileName: "Development")
    .DisableForwardedHeaders()
    .WithReplicas(3)
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("ENV", "development")
    .WithReference(db)
    .WithReference(payments)
    .WithArgs(new string[] { "--verbose", "--enable-swagger" })
    .WithHttpEndpoint(5000, null, "http", null, true)
    .WithHttpsEndpoint(5001, null, "https", null, true)
    .WithHttpHealthCheck("/health", 200, null)
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null)
    .WaitFor(db)
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null)
    .WithUrl("http://localhost:5000", "API Service")
    .WithHealthCheck("https://localhost:5001/health")
    .WithReferenceRelationship(apikey)
    .WithIconName("web", IconVariant.Filled);
var worker = builder.AddProject(name: "worker", projectPath: "../Worker/Worker.csproj", launchProfileName: "Development")
    .WithEnvironment("API_KEY", apikey)
    .WithReference(db)
    .WaitForStart(api)
    .WithParentRelationship(api);

builder.Build().Run();
