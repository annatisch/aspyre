#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithHttpsEndpoint(8443, null, "https", null, true);

builder.Build().Run();
