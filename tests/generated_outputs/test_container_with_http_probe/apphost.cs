#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROBES001
var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
