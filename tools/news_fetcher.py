import yfinance as yf
from crewai.tools import tool

@tool("Fetch Live Company News")
def fetch_company_news(ticker: str) -> str:
    """
    Fetches the latest business and financial news articles for a given stock ticker.
    Returns a structured string containing titles, publishers, links, and publishing times.
    """
    try:
        stock = yf.Ticker(ticker)
        news_list = stock.news
        
        if not news_list:
            return f"No recent news articles found for ticker: {ticker.upper()}."
            
        # Extract the top 8 most recent news articles
        formatted_news = f"--- Latest Financial News for {ticker.upper()} ---\n\n"
        
        for i, article in enumerate(news_list[:8], 1):
            # Dig into the new nested structure
            content = article.get("content", {})
            
            title = content.get("title", "No Title")
            publisher = content.get("provider", {}).get("displayName", "Unknown Publisher")
            
            # Safely grab the URL
            url_data = content.get("canonicalUrl", {})
            link = url_data.get("url", "No Link Available")
            
            formatted_news += f"{i}. Title: {title}\n"
            formatted_news += f"   Publisher: {publisher}\n"
            formatted_news += f"   URL: {link}\n\n"
            
        return formatted_news
        
    except Exception as e:
        return f"Error gathering news for {ticker}: {str(e)}"