#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

#pragma warning disable ASPIREPROXYENDPOINTS001
var mycontainer = builder.AddContainer("mycontainer", "nginx")
    .WithEndpointProxySupport(true);
#pragma warning restore ASPIREPROXYENDPOINTS001

builder.Build().Run();
