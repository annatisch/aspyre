#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "key123", false, true);
var mycontainer = builder.AddContainer("mycontainer", "myapp")
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("DEBUG", "true");

builder.Build().Run();
