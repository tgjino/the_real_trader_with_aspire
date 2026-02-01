namespace The_real_trader.Web;


public class TradingServiceClient(HttpClient httpClient)
{
    public async Task<Stock[]> GetStocksAsync()=>
        await httpClient.GetFromJsonAsync<Stock[]>("/stocks")??[];
}

public record Stock(string Symbol, decimal Price);