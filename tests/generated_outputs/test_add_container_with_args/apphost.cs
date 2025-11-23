#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithArgs(new string[] { "-g", "daemon off;" });

builder.Build().Run();
