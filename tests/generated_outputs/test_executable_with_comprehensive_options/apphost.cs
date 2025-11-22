
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py", "--verbose" })
    .WithCommand("python3")
    .WithWorkingDirectory("/app/src")
    .PublishAsDockerFile()
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("DEBUG", "true")
    .WithReference(db)
    .WithCertificateTrustScope(CertificateTrustScope.Append)
    .WithHttpEndpoint(8080, null, "http", null, true)
    .WithHttpsEndpoint(8443, null, "https", null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null)
    .WaitFor(db)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null)
    .WithUrl("http://localhost:8080")
    .WithIconName("terminal", IconVariant.Filled);

builder.Build().Run();
