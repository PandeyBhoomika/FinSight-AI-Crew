import os
from fpdf import FPDF
from datetime import datetime

def generate_pdf_report(report_text: str, ticker: str) -> str:
    """
    Takes the final text report from the AI Crew and generates a clean PDF.
    Saves it to the 'reports' directory and returns the file path.
    """
    try:
        # Ensure the reports directory exists
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add Title
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(0, 10, txt=f"AI Financial Analysis Report: {ticker.upper()}", ln=True, align='C')
        
        # Add Date
        pdf.set_font("Helvetica", style="I", size=10)
        date_str = datetime.now().strftime("%B %d, %Y")
        pdf.cell(0, 10, txt=f"Generated on: {date_str}", ln=True, align='C')
        pdf.ln(10) # Add a line break

        # Add Body Text
        pdf.set_font("Helvetica", size=11)
        
        # Clean text to prevent character encoding errors in FPDF
        report_clean = report_text.encode('latin-1', 'replace').decode('latin-1')
        
        # multi_cell handles line breaks automatically
        pdf.multi_cell(0, 7, txt=report_clean)
        
        # Generate filename with timestamp and save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{ticker.lower()}_analysis_{timestamp}.pdf"
        file_path = os.path.join(reports_dir, filename)
        
        pdf.output(file_path)
        return file_path
        
    except Exception as e:
        return f"Error generating PDF: {str(e)}"