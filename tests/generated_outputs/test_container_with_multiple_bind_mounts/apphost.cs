
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithBindMount(source: "/host/data", target: "/container/data", isReadOnly: false )
    .WithBindMount(source: "/host/config", target: "/container/config", isReadOnly: true );

builder.Build().Run();
