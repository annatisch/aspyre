
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080");
var primary = builder.AddConnectionString("primary");
var secondary = builder.AddConnectionString("secondary");
secondary.WithConnectionStringRedirection(primary.Resource);
secondary.WithUrl("http://localhost:5432");
secondary.WithIconName("database");

builder.Build().Run();
