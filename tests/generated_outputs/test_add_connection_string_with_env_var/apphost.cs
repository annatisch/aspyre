#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myconnection = builder.AddConnectionString(name: "myconnection", environmentVariableName: "MY_CONNECTION_STRING");

builder.Build().Run();
