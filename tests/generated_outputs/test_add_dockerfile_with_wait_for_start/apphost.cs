#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddContainer("service1", "postgres");
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WaitForStart(service1);

builder.Build().Run();
