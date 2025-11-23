#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithEnvironment("PORT", "8080");

builder.Build().Run();
