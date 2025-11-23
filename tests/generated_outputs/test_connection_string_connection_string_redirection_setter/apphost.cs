#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080");
var primary = builder.AddConnectionString("primary");
var secondary = builder.AddConnectionString("secondary");
var myconnection = builder.AddConnectionString("myconnection");
myconnection.WithConnectionStringRedirection(primary.Resource);
myconnection.WithConnectionStringRedirection(secondary.Resource);
myconnection.WithUrl("http://localhost:5432");
myconnection.WithUrl("http://localhost:5433");
myconnection.WithIconName("database");
myconnection.WithIconName("database2", IconVariant.Filled);

builder.Build().Run();
