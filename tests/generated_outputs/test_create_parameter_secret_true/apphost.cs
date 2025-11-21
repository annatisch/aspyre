
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mypassword = builder.CreateParameter("mypassword", true);

builder.Build().Run();
