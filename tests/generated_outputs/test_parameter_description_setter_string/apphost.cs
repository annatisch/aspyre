#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

var myconfig = builder.AddParameter(name: "myconfig", secret: false);
myconfig.WithDescription(description: "Configuration value", enableMarkdown: false);
myconfig.WithDescription(description: "Configuration value v2", enableMarkdown: false);

builder.Build().Run();
