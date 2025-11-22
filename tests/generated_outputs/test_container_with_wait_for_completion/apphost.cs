
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var config = builder.AddParameter("config", false);
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WaitForCompletion(config);

builder.Build().Run();
