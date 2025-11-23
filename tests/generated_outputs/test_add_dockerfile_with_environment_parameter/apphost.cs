#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var port = builder.AddParameter("port", "8080", false, false);
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithEnvironment("PORT", port);

builder.Build().Run();
