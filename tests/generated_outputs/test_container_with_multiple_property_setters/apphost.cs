#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString(name: "db", environmentVariableName: null);
var cache = builder.AddConnectionString(name: "cache", environmentVariableName: null);
var mycontainer = builder.AddContainer(name: "mycontainer", image: "nginx");
mycontainer.PublishAsContainer();
mycontainer.PublishAsContainer();
mycontainer.WithBindMount(source: "/host/path", target: "/container/path", isReadOnly: false);
mycontainer.WithBindMount(source: "/host/path", target: "/container/path", isReadOnly: true);
mycontainer.WithContainerName(name: "my-nginx-container");
mycontainer.WithContainerName(name: "another-name");
mycontainer.WithEntrypoint(entrypoint: "/app/entrypoint.sh");
mycontainer.WithEntrypoint(entrypoint: "/app/another-entrypoint.sh");
mycontainer.WithImage(image: "nginx:alpine", tag: null);
mycontainer.WithImage(image: "nginx", tag: "latest");
mycontainer.WithEnvironment(name: "PORT", value: "8080");
mycontainer.WithEnvironment(name: "PORT", value: "9090");
mycontainer.WithReference(source: db, connectionName: "db", optional: true);
mycontainer.WithReference(source: cache, connectionName: null, optional: false);
mycontainer.WithHttpEndpoint(port: 8080, targetPort: 80, name: "http", env: "env", isProxied: false);
mycontainer.WithHttpEndpoint(port: 9090, targetPort: null, name: "http-alt", env: null, isProxied: true);
mycontainer.WaitFor(dependency: db);
mycontainer.WaitFor(dependency: cache);

builder.Build().Run();
