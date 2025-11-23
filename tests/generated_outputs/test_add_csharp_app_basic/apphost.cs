#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myproject = builder.AddCSharpApp("myproject", "../MyProject/MyProject.csproj");

builder.Build().Run();
