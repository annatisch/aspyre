
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var version = builder.AddParameter("version", "1.0.0", false, false);
var environment = builder.AddParameter("environment", "production", false, false);
var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithBuildArg("VERSION", version)
    .WithBuildArg("ENV", environment);

builder.Build().Run();
