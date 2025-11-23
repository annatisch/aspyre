#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var dbhost = builder.AddParameterFromConfiguration("dbhost",  "ConnectionStrings:DbHost", false);

builder.Build().Run();
