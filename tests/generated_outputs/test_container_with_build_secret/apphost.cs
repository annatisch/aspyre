#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithBuildSecret("API_KEY", apikey);

builder.Build().Run();
