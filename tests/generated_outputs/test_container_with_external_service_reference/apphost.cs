
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var api = builder.AddExternalService("api", "https://api.example.com");
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithReference(api);

builder.Build().Run();
