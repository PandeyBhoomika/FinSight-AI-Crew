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

def get_research_agent(tools_list):
    return Agent(
        role='Market Researcher',
        goal='Gather the latest news, market sentiment, and macroeconomic factors affecting the target stock.',
        backstory='You are a seasoned Wall Street market researcher who spots early trends and understands market psychology before anyone else.',
        verbose=True,
        allow_delegation=False,
        tools=tools_list, # Tools will be injected by the orchestrator
        llm=llm
    )