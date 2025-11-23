#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROBES001
var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
