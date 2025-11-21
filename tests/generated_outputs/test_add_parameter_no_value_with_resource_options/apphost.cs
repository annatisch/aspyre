
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", true)
    .WithDescription("API Key for service")
    .ExcludeFromMcp()
    .WithIconName("security");

builder.Build().Run();
