#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddContainer(name: "postgres", image: "postgres", tag: "16")
    .WithVolume(name: "pgdata", target: "/var/lib/postgresql/data", isReadOnly: false)
    .WithLifetime(lifetime: ContainerLifetime.Persistent)
    .WithEnvironment(name: "POSTGRES_PASSWORD", value: "dev-password")
    .WithHttpEndpoint(port: 5432, targetPort: null, name: null, env: null, isProxied: true);
var redis = builder.AddContainer(name: "redis", image: "redis", tag: "7-alpine")
    .WithLifetime(lifetime: ContainerLifetime.Persistent)
    .WithHttpEndpoint(port: 6379, targetPort: null, name: null, env: null, isProxied: true);
var auth = builder.AddDockerfile(name: "auth", contextPath: "./services/auth", dockerfilePath: "Dockerfile", stage: "production")
    .WithHttpEndpoint(port: 8081, targetPort: null, name: null, env: null, isProxied: true)
    .WaitForStart(dependency: postgres)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: null)
    .ExcludeFromManifest();
var api = builder.AddDockerfile(name: "api", contextPath: "./services/api", dockerfilePath: "Dockerfile.multi", stage: "release")
    .WithHttpEndpoint(port: 8080, targetPort: null, name: null, env: null, isProxied: true)
    .WithHttpsEndpoint(port: 8443, targetPort: null, name: null, env: null, isProxied: true)
    .WaitForStart(dependency: postgres)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: null);

builder.Build().Run();
