#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var dbpassword = builder.AddParameterFromConfiguration("dbpassword",  "ConnectionStrings:DbPassword", true)
    .WithDescription("Database password from configuration", true)
    .WithHealthCheck("https://db.example.com/health")
    .WithIconName("database");

builder.Build().Run();
