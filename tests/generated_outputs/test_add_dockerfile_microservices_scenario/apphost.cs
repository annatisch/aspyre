#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddContainer("postgres", "postgres", "16")
    .WithLifetime(ContainerLifetime.Persistent)
    .WithVolume("pgdata", "/var/lib/postgresql/data", false)
    .WithEnvironment("POSTGRES_PASSWORD", "dev-password")
    .WithHttpEndpoint(5432, null, null, null, true);
var redis = builder.AddContainer("redis", "redis", "7-alpine")
    .WithLifetime(ContainerLifetime.Persistent)
    .WithHttpEndpoint(6379, null, null, null, true);
var auth = builder.AddDockerfile("auth", "./services/auth", "Dockerfile", "production")
    .WithHttpEndpoint(8081, null, null, null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WaitForStart(postgres)
    .ExcludeFromManifest();
var api = builder.AddDockerfile("api", "./services/api", "Dockerfile.multi", "release")
    .WithHttpEndpoint(8080, null, null, null, true)
    .WithHttpsEndpoint(8443, null, null, null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WaitForStart(postgres)
    .WaitForStart(redis)
    .WaitForStart(auth);

builder.Build().Run();
