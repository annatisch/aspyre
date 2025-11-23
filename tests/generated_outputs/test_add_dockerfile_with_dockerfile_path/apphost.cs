#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", "Dockerfile.production", null);

builder.Build().Run();
