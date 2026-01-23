
using Aspire.Hosting.Python;
var builder = DistributedApplication.CreateBuilder(args);

var tradingService = builder.AddPythonProject("trading-service", "../trading_service", "api_app.py")
                            .WithExternalHttpEndpoints();
var apiService = builder.AddProject<Projects.The_real_trader_ApiService>("apiservice");

builder.AddProject<Projects.The_real_trader_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService)
    .WithReference(tradingService);

builder.Build().Run();
