
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var primary = builder.AddConnectionString("primary");
var secondary = builder.AddConnectionString("secondary");
secondary.WithConnectionStringRedirection(primary.Resource);

builder.Build().Run();
