
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080");
var primary = builder.AddConnectionString("primary");
var myconnection = builder.AddConnectionString("myconnection", "DB_CONNECTION")
    .WithConnectionStringRedirection(primary.Resource)
    .WithUrl("http://localhost:5432")
    .WithHealthCheck("https://db.example.com/health")
    .WithIconName("database", IconVariant.Regular);

builder.Build().Run();
