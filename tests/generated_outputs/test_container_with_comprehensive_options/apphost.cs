
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var mycontainer = builder.AddContainer("mycontainer", "myapp", "1.0.0")
    .PublishAsContainer()
    .WithBindMount(source: "/host/data", target: "/app/data", isReadOnly: true )
    .WithContainerName("my-app-container")
    .WithEntrypoint("/app/start.sh")
    .WithImagePullPolicy(pullPolicy: ImagePullPolicy.Always)
    .WithLifetime(ContainerLifetime.Persistent)
    .WithVolume("appdata", "/app/data", false)
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("DEBUG", "true")
    .WithReference(db)
    .WithCertificateTrustScope(CertificateTrustScope.Append)
    .WithArgs(new string[] { "--verbose" })
    .WithHttpEndpoint(8080, null, "http", null, true)
    .WithHttpsEndpoint(8443, null, "https", null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null)
    .WaitFor(db)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null)
    .WithUrl("http://localhost:8080")
    .WithIconName("box", IconVariant.Filled);

builder.Build().Run();
