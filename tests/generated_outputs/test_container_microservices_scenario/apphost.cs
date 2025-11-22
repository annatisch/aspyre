
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
var rabbitmq = builder.AddContainer("rabbitmq", "rabbitmq", "3-management")
    .WithLifetime(ContainerLifetime.Persistent)
    .WithEnvironment("RABBITMQ_DEFAULT_USER", "admin")
    .WithEnvironment("RABBITMQ_DEFAULT_PASS", "admin")
    .WithHttpEndpoint(5672, null, null, null, true);
var auth = builder.AddContainer("auth", "myapp-auth", "latest")
    .WithHttpEndpoint(8081, null, null, null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WaitForStart(postgres);
var api = builder.AddContainer("api", "myapp-api", "latest")
    .WithHttpEndpoint(8080, null, null, null, true)
    .WithHttpsEndpoint(8443, null, null, null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null)
    .WaitForStart(postgres)
    .WaitForStart(redis)
    .WaitForStart(auth)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, null, null, null, null, null);
var worker = builder.AddContainer("worker", "myapp-worker", "latest")
    .WaitForStart(postgres)
    .WaitForStart(rabbitmq);

builder.Build().Run();
