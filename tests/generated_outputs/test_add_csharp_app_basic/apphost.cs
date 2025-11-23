#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIRECSHARPAPPS001
var myproject = builder.AddCSharpApp("myproject", "../MyProject/MyProject.csproj");
#pragma warning restore ASPIRECSHARPAPPS001

builder.Build().Run();
