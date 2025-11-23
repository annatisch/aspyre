#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExternalService("service1", "http://localhost:8080");
var service2 = builder.AddExternalService("service2", "http://localhost:6379")
    .WithChildRelationship(service1);

builder.Build().Run();
