from resume_match.generate_ai_competitor import AICompetitor
from resume_match.enhance_resume import AIResumeMatcher
from data.input import resume, jd

def main():
    print("Hello from backend!")
    ai_competitor = AICompetitor(resume, jd, 30)
    factors = ai_competitor.extract_factors()
    print("Extracted Factors:", factors)
    print()
    enhanced_resume = ai_competitor.generate_resume()
    print("Generated Enhanced Resume:", enhanced_resume)

def main_ats():
    print("Hello from backend ATS!")
    ai_competitor = AICompetitor(resume, jd, 30)
    # ats_keywords = ai_competitor.extract_ats_keywords()
    # #print("Extracted ATS Keywords:", ats_keywords)
    # print()
    ats_optimized_resume = ai_competitor.generate_ats_optimized_resume()
    print("Generated ATS Optimized Resume:", ats_optimized_resume)

    ## Create the resume in pdf format and add datetime stamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./backend/output/ats_optimized_resume_{timestamp}.pdf"
    with open(filename, "w") as f:
        f.write(ats_optimized_resume)

if __name__ == "__main__":
    #main()
    main_ats()
    #main_resume()