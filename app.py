import streamlit as st
import os
import glob
import sys
import re
from dotenv import load_dotenv
from agents.orchestrator import run_financial_crew
from tools.pdf_generator import generate_pdf_report

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("Missing API Key: Please configure your GOOGLE_API_KEY inside the '.env' file.")
    st.stop()

# --- Custom Class to Catch Agent Terminal Output ---
class StreamlitRedirect:
    def __init__(self, container):
        self.container = container
        self.text = ""

    def write(self, msg):
        # Remove ANSI color codes that CrewAI uses for terminal formatting
        clean_msg = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', msg)
        if clean_msg.strip():
            self.text += clean_msg + "\n"
            # Update the UI container with the latest log
            self.container.markdown(f"```text\n{self.text}\n```")

    def flush(self):
        pass

# --- Page Configurations ---
st.set_page_config(page_title="FinSight AI Crew", page_icon="📈", layout="centered")

st.title("📈 FinSight AI Crew")
st.markdown("### Autonomous Multi-Agent Financial Analysis System")
st.write("Enter a company stock ticker symbol below. The Orchestrator will coordinate a Market Researcher agent, a Data Analyst agent, and a Report Writer agent to assemble a comprehensive corporate analysis.")
st.markdown("---")

ticker = st.text_input(label="Company Ticker Symbol:", placeholder="e.g., TSLA, AAPL, MSFT, NVDA", max_chars=5).upper().strip()

if st.button("Launch Agent Analysis Crew", use_container_width=True):
    if ticker:
        st.info(f"🚀 Deploying Agent Crew to analyze {ticker}...")
        
        # UI Element for the Bonus Tip: Conversation Log
        with st.expander("🕵️‍♂️ Live Agent Conversation Log", expanded=True):
            log_container = st.empty()
            
        # Hijack the standard output to our Streamlit UI
        original_stdout = sys.stdout
        sys.stdout = StreamlitRedirect(log_container)
            
        try:
            # 1. Trigger the Multi-Agent Execution Chain
            raw_report_output = run_financial_crew(ticker)
            
            # Restore normal terminal output once finished
            sys.stdout = original_stdout
            
            st.success("✅ Analysis & Self-Verification Complete!")
            
            # 2. Render Text Output to UI (Deliverable: Live Dashboard)
            st.markdown("## 📄 Executive Investment Briefing")
            st.markdown(raw_report_output)
            
            # Render the Chart Image
            st.markdown("### 📊 Market Performance Trend")
            chart_files = glob.glob(f"charts/{ticker.lower()}*.png")
            
            if chart_files:
                latest_chart = max(chart_files, key=os.path.getctime)
                st.image(latest_chart, caption=f"Generated Trend Chart for {ticker}")
            else:
                st.info("No visual chart was generated for this report.")
            
            st.markdown("---")
            
            # 3. Compile the PDF Artifact (Deliverable: Output as PDF)
            with st.spinner("Formatting and compiling PDF report..."):
                saved_pdf_path = generate_pdf_report(raw_report_output, ticker)
            
            if os.path.exists(saved_pdf_path):
                with open(saved_pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Publication-Grade PDF Report",
                        data=pdf_file,
                        file_name=os.path.basename(saved_pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
                
        except Exception as e:
            sys.stdout = original_stdout # Ensure terminal is restored on error
            st.error(f"❌ An execution error occurred: {str(e)}")
            
    else:
        st.sidebar.warning("Please enter a valid ticker symbol before hitting launch.")