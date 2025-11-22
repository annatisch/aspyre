
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db");
var apikey = builder.AddParameter("apikey", "key123", false, false);
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" });
myapp.WithCommand("python3");
myapp.WithWorkingDirectory("/app/src");
myapp.PublishAsDockerFile();
myapp.WithEnvironment("API_KEY", apikey);
myapp.WithReference(db);
myapp.WithHttpEndpoint(8080, null, null, null, true);
myapp.WaitFor(db);
myapp.WithIconName("application");

builder.Build().Run();
