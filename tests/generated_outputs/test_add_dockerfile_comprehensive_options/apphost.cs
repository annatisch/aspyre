
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var version = builder.AddParameter("version", "1.0.0", false, false);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var myapp = builder.AddDockerfile("myapp", "./app", "docker/Dockerfile.production", "release")
    .PublishAsContainer()
    .WithBindMount(source: "/host/data", target: "/app/data", isReadOnly: true )
    .WithBuildArg("VERSION", version)
    .WithBuildSecret("API_KEY", apikey)
    .WithContainerName("my-app-container")
    .WithEntrypoint("/app/start.sh")
    .WithImagePullPolicy(pullPolicy: ImagePullPolicy.Always)
    .WithLifetime(ContainerLifetime.Persistent)
    .WithVolume("appdata", "/app/data", false)
    .WithEnvironment("DEBUG", "true")
    .WithReference(db)
    .WithArgs(new string[] { "--verbose" })
    .WithHttpEndpoint(8080, null, "http", null, true)
    .WithHttpsEndpoint(8443, null, "https", null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WaitFor(db)
    .WithUrl("http://localhost:8080")
    .WithIconName("box", IconVariant.Filled);

builder.Build().Run();
