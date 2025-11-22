
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var dbconfig = builder.AddParameter("dbconfig", false);
var myconnection = builder.AddConnectionString("myconnection")
    .WithReferenceRelationship(dbconfig)
    .WithIconName("database", IconVariant.Filled);

builder.Build().Run();
