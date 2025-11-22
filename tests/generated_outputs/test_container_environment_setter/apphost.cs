
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "myapp");
mycontainer.WithEnvironment("DEBUG", "true");

builder.Build().Run();
