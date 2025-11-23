#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-value", true, true);

builder.Build().Run();
