
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExternalService("myservice", "http://localhost:8080");
myservice.WithDockerfileBaseImage("mcr.microsoft.com/dotnet/sdk:8.0", "mcr.microsoft.com/dotnet/aspnet:8.0");

builder.Build().Run();
