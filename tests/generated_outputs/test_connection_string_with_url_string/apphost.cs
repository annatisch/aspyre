#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myconnection = builder.AddConnectionString("myconnection")
    .WithUrl("http://localhost:5432");

builder.Build().Run();
