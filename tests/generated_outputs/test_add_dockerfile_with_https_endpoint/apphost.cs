#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithHttpsEndpoint(8443, null, "https", null, true);

builder.Build().Run();
