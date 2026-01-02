from resume_match.generate_ai_competitor import AICompetitor
from resume_match.enhance_resume import AIResumeMatcher
from data.input import resume, jd
from tqdm import tqdm
import time
from fpdf import FPDF
import re

def text_to_pdf(text, output_filename):
    """Convert text content to PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(left=15, top=15, right=15)
    
    # Set font
    pdf.set_font("Helvetica", size=10)
    
    # Process text line by line
    lines = text.split('\n')
    
    for line in lines:
        # Skip very long lines or split them
        if len(line) > 500:
            # Split very long lines into chunks
            chunks = [line[i:i+100] for i in range(0, len(line), 100)]
            for chunk in chunks:
                pdf.multi_cell(0, 5, chunk)
            continue
            
        # Handle headers (lines with # or all caps)
        if line.startswith('#'):
            # Markdown headers
            if line.startswith('###'):
                pdf.set_font("Helvetica", 'B', 10)
                line = line.replace('###', '').strip()
            elif line.startswith('##'):
                pdf.set_font("Helvetica", 'B', 11)
                line = line.replace('##', '').strip()
            elif line.startswith('#'):
                pdf.set_font("Helvetica", 'B', 13)
                line = line.replace('#', '').strip()
            try:
                pdf.multi_cell(0, 6, line)
                pdf.ln(2)
            except:
                pass  # Skip problematic lines
            pdf.set_font("Helvetica", size=10)
        elif line.strip().isupper() and len(line.strip()) > 0 and len(line.strip()) < 50:
            # All caps headers
            pdf.set_font("Helvetica", 'B', 11)
            try:
                pdf.multi_cell(0, 6, line)
                pdf.ln(1)
            except:
                pass
            pdf.set_font("Helvetica", size=10)
        elif line.strip().startswith('*') or line.strip().startswith('-'):
            # Bullet points
            bullet_text = line.strip()[1:].strip()
            try:
                pdf.set_x(20)  # Indent
                pdf.multi_cell(0, 5, f"• {bullet_text}")
            except:
                # Fallback for problematic lines
                try:
                    pdf.set_x(20)
                    pdf.multi_cell(0, 5, bullet_text[:200] + "...")
                except:
                    pass
        elif line.strip():
            # Regular text - handle long lines
            try:
                if len(line) > 200:
                    # Break long lines
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 100:
                            current_line += word + " "
                        else:
                            if current_line:
                                pdf.multi_cell(0, 5, current_line.strip())
                            current_line = word + " "
                    if current_line:
                        pdf.multi_cell(0, 5, current_line.strip())
                else:
                    pdf.multi_cell(0, 5, line)
            except:
                pass  # Skip problematic lines
        else:
            # Empty line
            pdf.ln(3)
    
    # Save PDF
    pdf.output(output_filename)

def main():
    print("Hello from backend!")
    
    with tqdm(total=100, desc="📄 Resume Enhancement", ncols=80) as pbar:
        pbar.set_description("🔧 Initializing AI Competitor")
        ai_competitor = AICompetitor(resume, jd, 30)
        pbar.update(20)
        
        pbar.set_description("🔍 Extracting Factors")
        factors = ai_competitor.extract_factors()
        print("Extracted Factors:", factors)
        print()
        pbar.update(30)
        
        pbar.set_description("✨ Generating Enhanced Resume")
        enhanced_resume = ai_competitor.generate_resume()
        pbar.update(50)
        
        print("Generated Enhanced Resume:", enhanced_resume)

def main_ats():
    print("Hello from backend ATS!")
    start_time = time.time()
    with tqdm(total=100, desc="🎯 ATS Optimization", ncols=80) as pbar:
        pbar.set_description("🔧 Initializing AI Competitor")
        ai_competitor = AICompetitor(resume, jd, 30)
        pbar.update(10)
        
        pbar.set_description("⚡ Generating ATS Optimized Resume")
        ats_optimized_resume, recomendations = ai_competitor.generate_ats_optimized_resume()
        pbar.update(70)
        
        print("==============Generated ATS Optimized Resume==================")
        print(ats_optimized_resume)
        print("==============================================================")

        pbar.set_description("💾 Saving Files")
        ## Create the resume in pdf format and add datetime stamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./backend/output/ats_optimized_resume_{timestamp}.pdf"
        text_to_pdf(ats_optimized_resume, filename)

        recomendation_filename = f"./backend/output/ats_recommendations_{timestamp}.pdf"
        text_to_pdf(recomendations, recomendation_filename)
        pbar.update(20)
        
        print(f"\n✅ Files saved:")
        print(f"   📄 Resume: {filename}")
        print(f"   📋 Recommendations: {recomendation_filename}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\n⏱️  Total Time Taken: {elapsed_time:.2f} seconds")
        
if __name__ == "__main__":
    main_ats()
