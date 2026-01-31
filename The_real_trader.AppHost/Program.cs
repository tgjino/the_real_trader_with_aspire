using Aspire.Hosting;
using Aspire.Hosting.Python;
var builder = DistributedApplication.CreateBuilder(args);
builder.Configuration["DOTNET_DASHBOARD_UNSECURED_ALLOW_ANONYMOUS"] = "true";
builder.Configuration["ASPNETCORE_URLS"] = "http://0.0.0.0:15000";
builder.Configuration["DOTNET_DASHBOARD_OTLP_ENDPOINT_URL"] = "http://0.0.0.0:18888";
builder.Configuration["ASPIRE_ALLOW_UNSECURED_TRANSPORT"] = "true";

var redirectUri = builder.Configuration["Fyers:RedirectUri"] ?? "https://studious-spoon-v9p5xpvvwq53wxvw-5000.app.github.dev/callback";

var tradingService = builder.AddResource(new ContainerResource("trading-service"))
                            .WithDockerfile("../trading_service")
                            .WithHttpEndpoint(targetPort: 5000)
                            .WithExternalHttpEndpoints()
                            .WithEnvironment("client_id", builder.Configuration["Fyers:ClientId"])
                            .WithEnvironment("secret_key", builder.Configuration["Fyers:SecretKey"])
                            .WithEnvironment("redirect_uri",redirectUri)
                            .WithEnvironment("DB_PATH", "/app/trading.db");
                            
var apiService = builder.AddProject<Projects.The_real_trader_ApiService>("apiservice");

builder.AddProject<Projects.The_real_trader_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService)
    .WithEnvironment("TradingService__Url", tradingService.GetEndpoint("http"));
    
builder.Build().Run();
