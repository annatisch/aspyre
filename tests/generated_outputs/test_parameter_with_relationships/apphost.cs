
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var config1 = builder.AddParameter("config1", false);
var config2 = builder.AddParameter("config2", false)
    .WithReferenceRelationship(config1);

builder.Build().Run();
