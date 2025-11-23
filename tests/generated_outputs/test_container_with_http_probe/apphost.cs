#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null);

builder.Build().Run();
