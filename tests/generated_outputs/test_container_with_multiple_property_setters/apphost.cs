
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var apikey = builder.AddParameter("apikey", "key123", false, false);
var mycontainer = builder.AddContainer("mycontainer", "myapp");
mycontainer.WithEnvironment("API_KEY", apikey);
mycontainer.WithReference(db);
mycontainer.WithHttpEndpoint(8080, null, null, null, true);
mycontainer.WithBindMount("/host/data", "/container/data");
mycontainer.WithEntrypoint("/app/start.sh");
mycontainer.WithContainerName("custom-container");
mycontainer.WithLifetime(ContainerLifetime.Persistent);
mycontainer.WithVolume(null, "/app/data", false);
mycontainer.WaitFor(db);

builder.Build().Run();
