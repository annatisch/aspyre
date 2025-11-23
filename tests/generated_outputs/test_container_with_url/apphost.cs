#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithUrl("http://localhost:8080", "Web UI");

builder.Build().Run();
