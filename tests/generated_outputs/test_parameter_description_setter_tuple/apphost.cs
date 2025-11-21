
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myconfig = builder.AddParameter("myconfig", false);
myconfig.WithDescription("Configuration value", false);

builder.Build().Run();
