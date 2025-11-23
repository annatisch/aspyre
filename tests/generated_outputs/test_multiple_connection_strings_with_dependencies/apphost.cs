#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var primary = builder.AddConnectionString("primary", "PRIMARY_DB")
    .WithIconName("database", IconVariant.Filled);
var replica = builder.AddConnectionString("replica", "REPLICA_DB")
    .WithConnectionStringRedirection(primary.Resource);
var api = builder.AddExecutable("api", "python", "/app", new string[] { "api.py" })
    .WithReference(primary)
    .WithReference(replica)
    .WaitForStart(replica);

builder.Build().Run();
