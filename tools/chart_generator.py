import os
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from crewai.tools import tool

@tool("Generate Stock Trend Chart")
def generate_stock_chart(ticker: str, period: str = "6mo") -> str:
    """
    Generates a historical stock price line chart for a given ticker and saves it to disk.
    Valid periods include: 1mo, 3mo, 6mo, 1y.
    Returns the absolute path to the saved image file.
    """
    try:
        # Ensure the target directory exists
        chart_dir = "charts"
        if not os.path.exists(chart_dir):
            os.makedirs(chart_dir)
            
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"Error: No data available to plot for ticker {ticker}."
            
        # Initialize the plot layout cleanly
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot closing prices
        ax.plot(hist.index, hist['Close'], label='Closing Price', linewidth=2)
        
        # Calculate moving averages for context
        if len(hist) > 20:
            ma20 = hist['Close'].rolling(window=20).mean()
            ax.plot(hist.index, ma20, label='20-Day Moving Avg', linestyle='--', linewidth=1.5)
            
        # Format the appearance
        ax.set_title(f"{ticker.upper()} Stock Price Trend ({period})", fontsize=14, pad=15)
        ax.set_xlabel("Date", fontsize=11)
        ax.set_ylabel("Price (USD)", fontsize=11)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='best')
        
        # Format X-Axis dates based on the selected period window
        if period in ["1mo", "3mo"]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            
        fig.autofmt_xdate()
        
        # Save the file out cleanly
        file_path = os.path.join(chart_dir, f"{ticker.lower()}_{period}_trend.png")
        plt.savefig(file_path, bbox_inches='tight', dpi=150)
        plt.close(fig) # Clear memory references
        
        return f"Success: Chart saved successfully at '{file_path}'"
        
    except Exception as e:
        return f"Error generating chart for {ticker}: {str(e)}"