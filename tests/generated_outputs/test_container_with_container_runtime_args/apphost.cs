
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithContainerRuntimeArgs(new string[] { "--cpus", "2", "--memory", "1g" });

builder.Build().Run();
