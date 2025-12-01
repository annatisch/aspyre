#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter(name: "apikey", value: "secret-key", publishValueAsDefault: false, secret: true);
var version = builder.AddParameter(name: "version", value: "1.0.0", publishValueAsDefault: false, secret: false);
var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var myapp = builder.AddDockerfile(name: "myapp", contextPath: "./app", dockerfilePath: "docker/Dockerfile.production", stage: "release")
    .WithVolume(name: "appdata", target: "/app/data", isReadOnly: false)
    .WithBindMount(source: "/host/data", target: "/app/data", isReadOnly: false)
    .WithEntrypoint(entrypoint: "/app/start.sh")
    .WithLifetime(lifetime: ContainerLifetime.Persistent)
    .WithImagePullPolicy(pullPolicy: ImagePullPolicy.Always)
    .PublishAsContainer()
    .WithContainerName(name: "my-app-container")
    .WithBuildArg(name: "VERSION", value: version)
    .WithBuildSecret(name: "API_KEY", value: apikey)
    .WithEnvironment(name: "DEBUG", value: "true")
    .WithArgs(args: new string[] { "--verbose" })
    .WithReference(source: db, connectionName: (string?)null, optional: false)
    .WithHttpEndpoint(port: 8080, targetPort: null, name: "http", env: (string?)null, isProxied: true)
    .WithHttpsEndpoint(port: 8443, targetPort: null, name: "https", env: (string?)null, isProxied: true)
    .WaitFor(dependency: db)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: (string?)null)
    .WithUrl(url: "http://localhost:8080", displayText: (string?)null)
    .WithIconName(iconName: "box", iconVariant: IconVariant.Filled);

builder.Build().Run();
