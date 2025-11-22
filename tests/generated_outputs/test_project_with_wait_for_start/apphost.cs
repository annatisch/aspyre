
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var myservice = builder.AddExecutable("myservice", "python", "/app", new string[] { "app.py" });
var myproject = builder.AddProject(name: "myproject", projectPath: "../MyProject/MyProject.csproj", launchProfileName: null)
    .WaitForStart(myservice);

builder.Build().Run();
