
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var serviceurl = builder.AddParameter("serviceurl", "http://localhost:8080", false, false);
var myservice = builder.AddExternalService("myservice", serviceurl);

builder.Build().Run();
