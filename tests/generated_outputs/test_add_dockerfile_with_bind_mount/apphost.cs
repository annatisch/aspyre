
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithBindMount(source: "/host/path", target: "/container/path", isReadOnly: false );

builder.Build().Run();
