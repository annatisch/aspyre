
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var apikey = builder.AddParameter("apikey", "secret-key", false, true);
var dbpass = builder.AddParameter("dbpass", "db-secret", false, true);
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithBuildSecret("API_KEY", apikey)
    .WithBuildSecret("DB_PASSWORD", dbpass);

builder.Build().Run();
