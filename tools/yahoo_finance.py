import yfinance as yf
from crewai.tools import tool
import pandas as pd

@tool("Fetch Stock Financial KPIs")
def fetch_stock_kpis(ticker: str) -> str:
    """
    Fetches core financial metrics and KPIs for a given stock ticker.
    Use this to get metrics like Market Cap, P/E Ratio, EPS, Profit Margins, and Beta.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract common KPIs with fallbacks if missing
        kpis = {
            "Company Name": info.get("longName", "N/A"),
            "Current Price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio (Trailing)": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "EPS (Trailing)": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Profit Margin": info.get("profitMargins", "N/A"),
            "Beta": info.get("beta", "N/A")
        }
        
        # Format the output into a clean string for the agent
        summary = f"--- Financial KPIs for {ticker.upper()} ---\n"
        for key, value in kpis.items():
            if isinstance(value, float) and ("Margin" in key or "Yield" in key):
                summary += f"{key}: {value * 100:.2f}%\n"
            elif isinstance(value, (int, float)) and value > 1_000_000:
                summary += f"{key}: ${value:,}\n"
            else:
                summary += f"{key}: {value}\n"
                
        return summary
    except Exception as e:
        return f"Error fetching KPIs for {ticker}: {str(e)}"

@tool("Fetch Historical Stock Prices")
def fetch_historical_prices(ticker: str, period: str = "6mo") -> str:
    """
    Fetches historical stock pricing data for a given ticker.
    Valid periods include: 1mo, 3mo, 6mo, 1y, 2y, 5y.
    Returns the Open, High, Low, Close, and Volume details.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"No historical data found for ticker {ticker} over period {period}."
            
        # Keep relevant columns and get the latest sample points to avoid overwhelming the LLM window
        hist_trimmed = hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10)
        
        # Calculate brief summary stats
        max_close = hist['Close'].max()
        min_close = hist['Close'].min()
        current_close = hist['Close'].iloc[-1]
        
        summary = (
            f"--- Historical Performance Summary ({period}) ---\n"
            f"Highest Close: ${max_close:.2f}\n"
            f"Lowest Close: ${min_close:.2f}\n"
            f"Latest Close: ${current_close:.2f}\n\n"
            f"Last 10 Trading Days Data:\n"
            f"{hist_trimmed.to_string()}\n"
        )
        return summary
    except Exception as e:
        return f"Error fetching historical prices for {ticker}: {str(e)}"