#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var service1 = builder.AddExecutable("service1", "python", "/app", new string[] { "service1.py" });
var service2 = builder.AddExecutable("service2", "python", "/app", new string[] { "service2.py" })
    .WaitForStart(service1);

builder.Build().Run();
