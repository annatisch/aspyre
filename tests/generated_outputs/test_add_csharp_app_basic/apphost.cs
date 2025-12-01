#:sdk Aspire.AppHost.Sdk@13.0.1.0
#:package Aspire.Hosting@13.0.1.0
using System.Security.Cryptography.X509Certificates;

var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIRECSHARPAPPS001
var myproject = builder.AddCSharpApp(name: "myproject", path: "../MyProject/MyProject.csproj");
#pragma warning restore ASPIRECSHARPAPPS001

builder.Build().Run();
