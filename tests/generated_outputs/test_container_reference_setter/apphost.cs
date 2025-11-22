
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var mycontainer = builder.AddContainer("mycontainer", "myapp");
mycontainer.WithReference(db);

builder.Build().Run();
