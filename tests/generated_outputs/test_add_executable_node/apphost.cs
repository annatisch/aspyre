#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var nodeapp = builder.AddExecutable("nodeapp", "node", "/app", new string[] { "server.js" });

builder.Build().Run();
