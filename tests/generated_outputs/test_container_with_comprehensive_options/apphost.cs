#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
#pragma warning disable ASPIREPROBES001
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
    .WithUrl("http://localhost:8080")
    .WithIconName("box", IconVariant.Filled);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
