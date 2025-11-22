
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var external = builder.AddExternalService("external", "https://api.external.com");
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithReference(external)
    .WithHttpEndpoint(8080, null, null, null, true);

builder.Build().Run();
