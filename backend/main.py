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
    pdf.set_margins(left=20, top=20, right=20)
    
    # Set font
    pdf.set_font("Helvetica", size=10)
    
    # Process text line by line
    lines = text.split('\n')
    lines_written = 0
    lines_skipped = 0
    
    for line_num, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            pdf.ln(2)
            continue
        
        # Clean line - remove tabs and problematic characters
        clean_line = line.replace('\t', '    ').encode('latin-1', errors='ignore').decode('latin-1').strip()
        
        if not clean_line:
            continue
        
        # CRITICAL: Reset X position to left margin before each line
        pdf.set_x(pdf.l_margin)
        
        # Handle very long lines by wrapping them
        if len(clean_line) > 85:
            words = clean_line.split()
            wrapped_lines = []
            current = ""
            for word in words:
                test_line = current + " " + word if current else word
                if len(test_line) < 80:
                    current = test_line
                else:
                    if current:
                        wrapped_lines.append(current)
                    current = word
            if current:
                wrapped_lines.append(current)
            
            # Process wrapped lines
            for wrapped in wrapped_lines:
                try:
                    pdf.set_x(pdf.l_margin)  # Reset position
                    pdf.multi_cell(0, 5, wrapped)
                    lines_written += 1
                except Exception as e:
                    print(f"Line {line_num} wrapped failed: {str(e)[:50]}")
                    lines_skipped += 1
            continue
        
        # Handle headers (lines with # or all caps)
        if clean_line.startswith('#'):
            # Markdown headers
            level = clean_line.count('#', 0, 3)
            header_text = clean_line.lstrip('#').strip()
            try:
                pdf.set_x(pdf.l_margin)
                if level == 1:
                    pdf.set_font("Helvetica", 'B', 13)
                elif level == 2:
                    pdf.set_font("Helvetica", 'B', 11)
                else:
                    pdf.set_font("Helvetica", 'B', 10)
                pdf.multi_cell(0, 6, header_text)
                pdf.ln(2)
                pdf.set_font("Helvetica", size=10)
                lines_written += 1
            except Exception as e:
                print(f"Header line {line_num} failed: {str(e)[:50]}")
                pdf.set_font("Helvetica", size=10)
                lines_skipped += 1
        elif clean_line.isupper() and 3 < len(clean_line) < 50:
            # All caps headers
            try:
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", 'B', 11)
                pdf.multi_cell(0, 6, clean_line)
                pdf.ln(1)
                pdf.set_font("Helvetica", size=10)
                lines_written += 1
            except Exception as e:
                print(f"Caps header line {line_num} failed: {str(e)[:50]}")
                pdf.set_font("Helvetica", size=10)
                lines_skipped += 1
        elif clean_line.startswith(('*', '-')):
            # Bullet points - use simple bullet without special character
            bullet_text = clean_line[1:].strip()
            try:
                pdf.set_x(pdf.l_margin + 5)  # Slight indent
                pdf.multi_cell(0, 5, f"- {bullet_text}")  # Use dash instead of bullet
                lines_written += 1
            except Exception as e:
                print(f"Bullet line {line_num} failed: {str(e)[:50]}")
                lines_skipped += 1
        else:
            # Regular text
            try:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 5, clean_line)
                lines_written += 1
            except Exception as e:
                print(f"Regular line {line_num} failed: {str(e)[:50]} | Content: {clean_line[:50]}")
                lines_skipped += 1
    
    # Save PDF
    pdf.output(output_filename)
    print(f"\nPDF Statistics: {lines_written} lines written, {lines_skipped} lines skipped out of {len(lines)} total")

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
