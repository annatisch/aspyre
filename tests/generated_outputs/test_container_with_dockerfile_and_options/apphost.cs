
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithDockerfile("Dockerfile.multi", "docker/Dockerfile", "production");

builder.Build().Run();
