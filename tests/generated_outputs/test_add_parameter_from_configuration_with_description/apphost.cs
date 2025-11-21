
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var dbhost = builder.AddParameterFromConfiguration("dbhost",  "ConnectionStrings:DbHost", false)
    .WithDescription("Database host from config");;

builder.Build().Run();
