#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var cache = builder.AddConnectionString("cache");
var mycontainer = builder.AddContainer("mycontainer", "nginx");
mycontainer.PublishAsContainer();
mycontainer.PublishAsContainer();
mycontainer.WithBindMount("/host/path", "/container/path");
mycontainer.WithBindMount("/host/path", "/container/path", true);
mycontainer.WithContainerName("my-nginx-container");
mycontainer.WithContainerName("another-name");
mycontainer.WithEntrypoint("/app/entrypoint.sh");
mycontainer.WithEntrypoint("/app/another-entrypoint.sh");
mycontainer.WithImage("nginx:alpine");
mycontainer.WithImage("nginx", "latest");
mycontainer.WithEnvironment("PORT", "8080");
mycontainer.WithEnvironment("PORT", "9090");
mycontainer.WithReference(db);
mycontainer.WithReference(cache);
mycontainer.WithHttpEndpoint(8080, 80, "http", "env", false);
mycontainer.WithHttpEndpoint(9090, null, "http-alt", null, true);
mycontainer.WaitFor(db);
mycontainer.WaitFor(cache);

builder.Build().Run();
