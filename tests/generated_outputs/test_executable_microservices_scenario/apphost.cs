#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var dbpassword = builder.AddParameter(name: "dbpassword", value: "supersecret", publishValueAsDefault: false, secret: true);
var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var redis = builder.AddConnectionString(name: "redis", environmentVariableName: "REDIS_URL");
var gateway = builder.AddExecutable(name: "gateway", command: "node", workingDirectory: "/app", args: new string[] { "gateway.js" })
    .WithHttpEndpoint(port: 8080, targetPort: null, name: "http", env: null, isProxied: true)
    .WithHttpHealthCheck(path: "/health", statusCode: null, endpointName: null)
    .WithIconName(iconName: "web", iconVariant: IconVariant.Filled);
var userservice = builder.AddContainer(name: "userservice", image: "python", tag: "/app");
var products = builder.AddExecutable(name: "products", command: "python", workingDirectory: "/app", args: new string[] { "product_service.py" })
    .WithEnvironment(name: "DB_PASSWORD", parameter: dbpassword)
    .WithReference(source: db, connectionName: null, optional: false)
    .WithHttpEndpoint(port: 8002, targetPort: null, name: null, env: null, isProxied: true)
    .WaitFor(dependency: db);
var orders = builder.AddExecutable(name: "orders", command: "python", workingDirectory: "/app", args: new string[] { "order_service.py" })
    .WithEnvironment(name: "DB_PASSWORD", parameter: dbpassword)
    .WithReference(source: redis, connectionName: null, optional: false)
    .WithHttpEndpoint(port: 8003, targetPort: null, name: null, env: null, isProxied: true)
    .WaitForStart(dependency: userservice)
    .WithParentRelationship(parent: userservice);
gateway.WaitForStart(dependency: userservice);
gateway.WaitForStart(dependency: products);
gateway.WaitForStart(dependency: orders);

builder.Build().Run();
