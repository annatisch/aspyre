#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREDOCKERFILEBUILDER001
var myservice = builder.AddExternalService("myservice", "http://localhost:8080")
    .WithDockerfileBaseImage();
#pragma warning restore ASPIREDOCKERFILEBUILDER001

builder.Build().Run();
