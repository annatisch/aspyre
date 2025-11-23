#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var dbhost = builder.AddParameter("dbhost", false);
var dbport = builder.AddParameter("dbport", false);
var dbservice = builder.AddExternalService("dbservice", "http://localhost:5432");
var myconnection = builder.AddConnectionString("myconnection")
    .WithReferenceRelationship(dbhost)
    .WithReferenceRelationship(dbport)
    .WithParentRelationship(dbservice);

builder.Build().Run();
