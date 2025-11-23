#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var db = builder.AddConnectionString("db", "DATABASE_URL");
var telemetry = builder.AddConnectionString("telemetry", "TELEMETRY_URL");
var api = builder.AddExecutable("api", "python", "/app", new string[] { "api.py", "--port", "8000" })
    .WithReference(db)
    .WithHttpEndpoint(8000, null, null, null, true)
    .WaitFor(db);
var worker = builder.AddExecutable("worker", "python", "/app", new string[] { "worker.py" })
    .WithReference(db)
    .WithReference(telemetry)
    .WaitForStart(api);

builder.Build().Run();
