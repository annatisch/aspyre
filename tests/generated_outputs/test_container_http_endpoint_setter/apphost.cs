
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx");
mycontainer.WithHttpEndpoint(8080, null, null, null, true);

builder.Build().Run();
