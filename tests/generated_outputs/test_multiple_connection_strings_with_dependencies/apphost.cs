#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var primary = builder.AddConnectionString(name: "primary", environmentVariableName: "PRIMARY_DB")
    .WithIconName(iconName: "database", iconVariant: IconVariant.Filled);
var replica = builder.AddConnectionString(name: "replica", environmentVariableName: "REPLICA_DB")
    .WithConnectionStringRedirection(resource: primary.Resource);
var api = builder.AddExecutable(name: "api", command: "python", workingDirectory: "/app", args: new string[] { "api.py" })
    .WithReference(source: primary, connectionName: (string?)null, optional: false)
    .WaitForStart(dependency: replica);

builder.Build().Run();
