
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-value", true, true)
    .WithDescription("API Key", false)
    .ExcludeFromManifest()
    .WithIconName("key", IconVariant.Regular);

builder.Build().Run();
