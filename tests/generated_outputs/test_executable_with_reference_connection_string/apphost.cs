#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: "DATABASE_URL");
var myapp = builder.AddExecutable(name: "myapp", command: "python", workingDirectory: "/app", args: new string[] { "app.py" })
    .WithReference(source: db, connectionName: (string?)null, optional: false);

builder.Build().Run();
