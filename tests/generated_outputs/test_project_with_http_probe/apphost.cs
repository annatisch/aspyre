#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROBES001
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WithHttpProbe(ProbeType.Readiness, "/ready", null, 10, null, null, null, null);
#pragma warning restore ASPIREPROBES001

builder.Build().Run();
