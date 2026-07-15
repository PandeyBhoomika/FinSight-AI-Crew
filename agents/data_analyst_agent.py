from crewai import Agent
from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

# Fixed import spacing and updated to CrewAI native LLM
# Updated to use the currently active Gemini model
llm = LLM(
    model="gemini/gemini-3.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY")
)

def get_data_analyst_agent(tools_list):
    """
    Configures and returns the Data Analyst Agent.
    Expects a list containing the yfinance and chart generation tools.
    """
    return Agent(
        role='Financial Data Analyst',
        goal='Analyze historical pricing records, compute critical financial KPIs, and generate visual market trends.',
        backstory=(
            'You are an expert quantitative analyst and data scientist. You look past market hype '
            'and rely strictly on numbers, moving averages, valuation ratios, and statistical data '
            'to evaluate a company\'s true performance trajectory.'
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools_list, # Injected by the orchestrator
        llm=llm
    )