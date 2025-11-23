#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080")
    .WithIconName("database", IconVariant.Regular);

builder.Build().Run();
