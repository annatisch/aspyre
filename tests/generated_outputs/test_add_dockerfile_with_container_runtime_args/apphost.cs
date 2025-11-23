#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddDockerfile("myapp", "./app", null, null)
    .WithContainerRuntimeArgs(new string[] { "--cpus", "2", "--memory", "1g" });

builder.Build().Run();
