
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var version = builder.AddParameter("version", "1.0.0", false, false);
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithBuildArg("VERSION", version);

builder.Build().Run();
