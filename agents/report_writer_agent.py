from crewai import Agent
from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

# Fixed import spacing and LLM setup
# Updated to use the currently active Gemini model
llm = LLM(
    model="gemini/gemini-3.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY")
)

def get_report_writer_agent():
    """
    Configures and returns the Report Writer Agent.
    This agent relies strictly on advanced reasoning and synthesis,
    so it does not require external data execution tools.
    """
    return Agent(
        role='Financial Report Writer',
        goal='Synthesize complex market research data and quantitative analytics into a professional investment report.',
        backstory=(
            'You are an elite financial journalist and investment communications expert. '
            'You specialize in turning dense numerical findings and disparate news streams '
            'into beautifully written, high-level executive summaries that give C-suite executives '
            'and retail investors clear, actionable insights.'
        ),
        verbose=True,
        allow_delegation=False,
        tools=[], # No tools required; operates purely on intelligence & context integration
        llm=llm
    )