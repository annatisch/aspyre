#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var apikey = builder.AddParameter("apikey", "key123", false, false);
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" });
myapp.WithCommand("python3");
myapp.WithCommand("python3 -u");
myapp.WithWorkingDirectory("/app/src");
myapp.WithWorkingDirectory("/app/src/v2");
myapp.PublishAsDockerFile();
myapp.WithEnvironment("API_KEY", apikey);
myapp.WithEnvironment("DEBUG", "true");
myapp.WithReference(db);
myapp.WithHttpEndpoint(8080, null, "http", null, true);
myapp.WithHttpEndpoint(8081, null, "http-alt", null, true);
myapp.WaitFor(db);
myapp.WaitFor(apikey);
myapp.WithIconName("application");
myapp.WithIconName("application", IconVariant.Filled);

builder.Build().Run();
