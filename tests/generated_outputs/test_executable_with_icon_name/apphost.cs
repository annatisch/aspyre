
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myapp = builder.AddExecutable("myapp", "python", "/app", null)
    .WithIconName("terminal", IconVariant.Regular);

builder.Build().Run();
