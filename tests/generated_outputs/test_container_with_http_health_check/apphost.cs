#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithHttpHealthCheck("/health", 200, null);

builder.Build().Run();
