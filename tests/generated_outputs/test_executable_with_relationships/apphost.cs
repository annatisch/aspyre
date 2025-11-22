
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var config = builder.AddParameter("config", false);
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithReferenceRelationship(config);

builder.Build().Run();
