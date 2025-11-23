#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithBindMount(source: "/host/data", target: "/container/data", isReadOnly: false )
    .WithBindMount(source: "/host/config", target: "/container/config", isReadOnly: true );

builder.Build().Run();
