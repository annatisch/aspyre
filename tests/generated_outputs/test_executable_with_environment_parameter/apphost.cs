#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var port = builder.AddParameter("port", "8080", false, false);
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithEnvironment("PORT", port);

builder.Build().Run();
