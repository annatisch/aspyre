#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myconnection = builder.AddConnectionString("myconnection")
    .WithHealthCheck("https://db.example.com/health");

builder.Build().Run();
