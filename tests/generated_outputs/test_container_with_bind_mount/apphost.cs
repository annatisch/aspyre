
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithBindMount(source: "/host/path", target: "/container/path", isReadOnly: false );

builder.Build().Run();
