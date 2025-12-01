#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: (string?)null);
var apikey = builder.AddParameter(name: "apikey", value: "key123", publishValueAsDefault: false, secret: false);
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj");
myproject.WithReplicas(replicas: 2);
myproject.WithReplicas(replicas: 4);
myproject.DisableForwardedHeaders();
myproject.DisableForwardedHeaders();
myproject.WithEnvironment(name: "API_KEY", parameter: apikey);
myproject.WithEnvironment(name: "API_KEY", value: (string?)null);
myproject.WithHttpEndpoint(port: 8080, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);
myproject.WithHttpEndpoint(port: 8081, targetPort: null, name: (string?)null, env: (string?)null, isProxied: true);
myproject.WaitFor(dependency: db);
myproject.WaitFor(dependency: apikey);
myproject.WithIconName(iconName: "application", iconVariant: IconVariant.Filled);
myproject.WithIconName(iconName: "application", iconVariant: IconVariant.Filled);

builder.Build().Run();
