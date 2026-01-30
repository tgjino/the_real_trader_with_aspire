
using Aspire.Hosting.Python;
var builder = DistributedApplication.CreateBuilder(args);

var tradingService = builder.AddPythonProject("trading-service", "../trading_service", "api_app.py")
                            .WithExternalHttpEndpoints(port: 5000, name: "http")
                            .WithEnvironment("PORT", "5000")
                            .WithEnvironment("client_id", builder.Configuration["Fyers:ClientId"])
                            .WithEnvironment("secret_key", builder.Configuration["Fyers:SecretKey"])
                            .WithEnvironment("redirect_uri", "https://studious-spoon-v9p5xpvvwq53wxvw-5000.app.github.dev/callback")
                            .WithDataVolume("trading_storage", "/app/data")
                            .WithEnvironment("DB_PATH", "/app/data/trading.db");
                            
var apiService = builder.AddProject<Projects.The_real_trader_ApiService>("apiservice");

builder.AddProject<Projects.The_real_trader_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService)
    .WithReference(tradingService);
    
builder.Build().Run();
