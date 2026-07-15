from crewai import Task, Crew, Process
from agents.market_research_agent import get_research_agent
from agents.data_analyst_agent import get_data_analyst_agent
from agents.report_writer_agent import get_report_writer_agent

# Import all the specialized tools we built
from tools.yahoo_finance import fetch_stock_kpis, fetch_historical_prices
from tools.news_fetcher import fetch_company_news
from tools.sentiment import analyze_financial_sentiment
from tools.chart_generator import generate_stock_chart

def run_financial_crew(ticker: str) -> str:
    """
    Orchestrates the multi-agent execution flow.
    Gathers research, performs analytical calculations, creates charts, 
    outputs a compiled financial analysis, and self-verifies the output.
    """
    
    # 1. Distribute tools to respective agents
    research_tools = [fetch_company_news, analyze_financial_sentiment]
    analyst_tools = [fetch_stock_kpis, fetch_historical_prices, generate_stock_chart]
    
    # 2. Instantiate the agent personas
    market_researcher = get_research_agent(research_tools)
    data_analyst = get_data_analyst_agent(analyst_tools)
    report_writer = get_report_writer_agent()
    
    # 3. Define the step-by-step sequential tasks
    research_task = Task(
        description=(
            f"Collect the latest financial news for ticker '{ticker.upper()}'. "
            f"Pass these headlines into the sentiment analysis tool to determine the prevailing market outlook. "
            f"Identify any major upcoming events, product announcements, or macroeconomic headwinds."
        ),
        expected_output="A structured markdown report detailing top headlines, market mood, and structural drivers.",
        agent=market_researcher
    )

    analysis_task = Task(
        description=(
            f"Gather essential KPIs and historical price sheets for ticker '{ticker.upper()}'. "
            f"Trigger the chart generation tool to draw and save the 6-month historical line chart. "
            f"Analyze basic moving patterns, valuation premiums, and margins."
        ),
        expected_output="A summary table of fundamental metrics, price action interpretation, and verification of chart production.",
        agent=data_analyst
    )

    writing_task = Task(
        description=(
            f"Synthesize all discoveries compiled by the Market Researcher and Data Analyst for '{ticker.upper()}'. "
            f"Format a draft 4-paragraph executive investment briefing. "
            f"Conclude with a clear, definitive recommendation outlook (e.g., Buy, Sell, or Hold) supported by the data."
        ),
        expected_output="A drafted, professionally written text report ready for review.",
        agent=report_writer
    )

    # NEW: The Self-Verification / Error Correction Task
    verification_task = Task(
        description=(
            f"Critically review the drafted executive briefing for '{ticker.upper()}'. "
            f"Self-verify the logic: Do the sentiment analysis and KPIs actively support the final recommendation? "
            f"Check for any hallucinated numbers. Correct any contradictory statements before final delivery."
        ),
        expected_output="A finalized, error-checked, and verified investment report ready for PDF compilation.",
        agent=report_writer
    )

    # 4. Form the Team Crew assembly
    crew = Crew(
        agents=[market_researcher, data_analyst, report_writer],
        tasks=[research_task, analysis_task, writing_task, verification_task],
        process=Process.sequential,
        verbose=True,
        max_rpm=15 # Prevents hitting API rate limits during high collaboration
    )

    # Kick off the synchronous crew operation
    result = crew.kickoff()
    
    # Return the clean string content output from the final task
    return str(result)