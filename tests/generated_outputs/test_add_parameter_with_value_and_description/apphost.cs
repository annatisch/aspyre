#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "default-value", false, false)
    .WithDescription("API Key configuration");

builder.Build().Run();
