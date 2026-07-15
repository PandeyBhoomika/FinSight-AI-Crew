import os
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize an internal instance of Gemini specifically for sentiment parsing
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

@tool("Analyze Financial Sentiment")
def analyze_financial_sentiment(text_content: str) -> str:
    """
    Performs Natural Language Processing (NLP) sentiment analysis on a block of text, 
    headlines, or social media statements.
    Returns a structured summary breakdown including sentiment classification (Positive/Negative/Neutral) 
    and a short rationale.
    """
    if not text_content.strip():
        return "Error: No text provided for sentiment analysis."

    prompt = (
        f"You are an expert financial sentiment analysis system.\n"
        f"Analyze the following financial news headlines or content and provide a clean summary.\n"
        f"Determine if the overall sentiment is Bullish (Positive), Bearish (Negative), or Neutral.\n"
        f"Provide a sentiment score from -1.0 (extremely bearish) to +1.0 (extremely bullish).\n\n"
        f"Content to analyze:\n{text_content}\n\n"
        f"Response Format:\n"
        f"- Overall Sentiment: [Bullish/Bearish/Neutral]\n"
        f"- Sentiment Score: [Score between -1.0 and 1.0]\n"
        f"- Key Drivers: [Briefly list 2-3 main keywords or events driving this sentiment]"
    )
    
    try:
        response = llm.invoke(prompt)
        return f"--- Financial Sentiment Analysis --- \n\n{response.content}"
    except Exception as e:
        return f"Error running sentiment analysis: {str(e)}"