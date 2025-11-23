#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myconfig = builder.AddParameter("myconfig", false);
myconfig.WithDescription("Configuration value");
myconfig.WithDescription("Configuration value v2", false);

builder.Build().Run();
