#:sdk Aspire.AppHost.Sdk@13.0.0


var builder = DistributedApplication.CreateBuilder(args);

var dbpassword = builder.AddParameter("dbpassword", "supersecret", false, true);
var db = builder.AddConnectionString("db", "DATABASE_URL");
var redis = builder.AddConnectionString("redis", "REDIS_URL");
var gateway = builder.AddExecutable("gateway", "node", "/app", new string[] { "gateway.js" })
    .WithHttpEndpoint(8080, null, "http", null, true)
    .WithHttpHealthCheck("/health", null, null)
    .WithIconName("web", IconVariant.Filled);
#pragma warning disable ASPIREPROBES001
var users = builder.AddExecutable("users", "python", "/app", new string[] { "user_service.py" })
    .WithEnvironment("DB_PASSWORD", dbpassword)
    .WithReference(db)
    .WithReference(redis)
    .WithHttpEndpoint(8001, null, null, null, true)
    .WithHttpProbe(ProbeType.Liveness, "/alive", null, null, null, null, null, null)
    .WaitFor(db);
#pragma warning restore ASPIREPROBES001
var products = builder.AddExecutable("products", "python", "/app", new string[] { "product_service.py" })
    .WithEnvironment("DB_PASSWORD", dbpassword)
    .WithReference(db)
    .WithHttpEndpoint(8002, null, null, null, true)
    .WaitFor(db);
var orders = builder.AddExecutable("orders", "python", "/app", new string[] { "order_service.py" })
    .WithEnvironment("DB_PASSWORD", dbpassword)
    .WithReference(db)
    .WithHttpEndpoint(8003, null, null, null, true)
    .WaitForStart(users)
    .WaitForStart(products)
    .WithParentRelationship(users)
    .WithParentRelationship(products);
gateway.WaitForStart(users);
gateway.WaitForStart(products);
gateway.WaitForStart(orders);

builder.Build().Run();
