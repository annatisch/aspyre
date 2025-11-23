#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080")
    .WithHealthCheck("https://localhost:8080/health");

builder.Build().Run();
