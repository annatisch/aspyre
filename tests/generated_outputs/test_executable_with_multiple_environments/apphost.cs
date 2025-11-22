
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "key123", false, true);
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithEnvironment("API_KEY", apikey)
    .WithEnvironment("DEBUG", "true");

builder.Build().Run();
