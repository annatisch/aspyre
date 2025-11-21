
#:sdk Aspire.AppHost.Sdk@13.0.0

var builder = DistributedApplication.CreateBuilder(args);

var mypassword = builder.AddParameter("mypassword", true);
mypassword.WithDescription("Secret password", true);

builder.Build().Run();
