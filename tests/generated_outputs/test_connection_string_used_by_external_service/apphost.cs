#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var dbconnection = builder.AddConnectionString("dbconnection", "DB_CONNECTION_STRING");
var api = builder.AddExternalService("api", "http://localhost:8080")
    .WithReferenceRelationship(dbconnection);

builder.Build().Run();
