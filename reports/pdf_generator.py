from fpdf import FPDF
import os

class PDFReportGenerator:
    def __init__(self, output_dir="reports/pdfs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_pdf(self, report_text, filename="report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        
        # Header - Ankit Singh name bold and big
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(0, 20, "Ankit Singh", ln=True, align="C")
        
        # Some spacing
        pdf.ln(10)
        
        # Body - Report text
        pdf.set_font("Arial", '', 14)
        for line in report_text.split('\n'):
            pdf.cell(0, 10, line, ln=True)
        
        # Save PDF file
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        print(f"PDF saved at {filepath}")
        return filepath

# Example usage:
if __name__ == "__main__":
    report = """Daily Profit Target: $100
Total Trades: 10
Wins: 7
Losses: 3
Accuracy: 70%
Performance: GOOD
"""
    generator = PDFReportGenerator()
    generator.generate_pdf(report, filename="daily_report.pdf")
