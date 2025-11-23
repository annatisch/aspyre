#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "postgres")
    .WithVolume("pgdata", "/var/lib/postgresql/data", false);

builder.Build().Run();
