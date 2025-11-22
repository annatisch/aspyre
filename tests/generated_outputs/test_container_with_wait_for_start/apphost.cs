
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddContainer("service1", "postgres");
var service2 = builder.AddContainer("service2", "myapp")
    .WaitForStart(service1);

builder.Build().Run();
