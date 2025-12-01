#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var serviceurl = builder.AddParameter(name: "serviceurl", value: "http://localhost:8080", publishValueAsDefault: false, secret: false);
var myservice = builder.AddExternalService(name: "myservice", urlParameter: serviceurl);

builder.Build().Run();
