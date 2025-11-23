#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddContainer("postgres", "postgres", "16");
var redis = builder.AddContainer("redis", "redis", "7");
var webapp = builder.AddContainer("webapp", "myapp")
    .WaitForStart(postgres)
    .WaitForStart(redis);

builder.Build().Run();
