
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable("myapp", "python", "/app", new string[] { "app.py" })
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null)
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null);

builder.Build().Run();
