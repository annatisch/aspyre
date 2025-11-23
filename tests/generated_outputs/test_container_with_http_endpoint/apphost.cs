#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithHttpEndpoint(8080, null, "http", null, true);

builder.Build().Run();
