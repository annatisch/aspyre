
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var dbpassword = builder.AddParameterFromConfiguration("dbpassword",  "ConnectionStrings:DbPassword", true);

builder.Build().Run();
