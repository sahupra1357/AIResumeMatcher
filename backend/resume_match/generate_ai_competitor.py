import sys
from pathlib import Path
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.model import generate_llm_response, generate_embedding
from data.input import resume, jd
from resume_match.ats_scorer import ATSScorer
from resume_match.skill_comparison import SkillComparison

from resume_match.observability import init_observability
# Initialize observability
init_observability()

class AICompetitor:
    def __init__(self, resume_text, job_description, difficulty_level):
        self.resume_text = resume_text
        self.job_description = job_description
        self.difficulty_level = int(difficulty_level)
        self.generated_resume = None
        self.factors = None
        self.ats_keywords = self.extract_ats_keywords(self.job_description)
        self.RESUME_OUTPUT_CONTRACT = """
                CRITICAL OUTPUT RULES (ABSOLUTE):
                - Return ONLY the resume text
                - NO explanations, notes, tips, commentary, headings, or analysis
                - NO preamble or postscript
                - NO bullet points explaining changes
                - Start directly with the resume header
                - End with the last resume line
                - If unsure, still output ONLY the resume
                """
        self.skill_comparison = SkillComparison(resume_text, job_description, self.ats_keywords)

    def extract_factors(self):
        if self.factors:
            return self.factors
        
        SYSTEM_PROMPT = """
        You are an expert job analysis AI specialist in distilling job description to their core requirements.  
        Your task is analyze the job description and extract most critical factors that will determmine success in this role.Focous on extracting:
              1. Required technical skills: the specific technical abilities and knowledge in domain for the position.
              2. Key responsibilties: The main tasks and responsibilities that form core of the job.
        Only include specific and relevant terms (e.g 'machine learning', 'data analysis', 'project management', 'cloud computing', 'cybersecurity') that are directly related to the job role.Avoid vague or general tems like 'team player' or 'communication skills'.
        Your output must be a valid list in format: ["factor1", "factor2", "factor3", "factor4", "factor5"]
        """

        USER_PROMPT = f"""
        Extract all key factors (each max 2 words) that most strongly infuence the job role describe below.and
        Job Description: {self.job_description}
        """

        self.factors = generate_llm_response(SYSTEM_PROMPT, USER_PROMPT, llm_type="openai_reasoning")

        return self.factors
    
    def determine_enhancement(self):
        if self.difficulty_level <= 20:
            self.enhancement_description = "slightly more impressive"
            self.intensity = "modest"
        elif self.difficulty_level <= 40:
            self.enhancement_descrition = "moderately more impressive"
            self.intensity = "significant"
        elif self.difficulty_level <= 60:
            self.enhancement_descrition = "substantially more impressive"
            self.intensity = "extensive"
        elif self.difficulty_level <= 80:
            self.enhancement_descrition = "dramatically more impressive"
            self.intensity = "comprehensive"
        return (self.enhancement_descrition, self.intensity)
    

    def generate_resume(self):
        if self.generated_resume:
            return self.generated_resume
        
        if not hasattr(self, 'enhancement_descrition') or not hasattr(self, 'intensity'):
            self.determine_enhancement()
        
        SYSTEM_PROMPT = f"""
        You are an expert resume enhancer AI specialist tasked with creating a stronger competitor version of candidate's resume.

        Your job is to create a resume that is {self.enhancement_descrition} than the original (approximately {self.difficulty_level}% stronger) by:
        1. Enhance technical skills with {self.intensity} additions of relevant technologies and framworks.
        2. Updating project descriptions with more advanced concept and technical depth
        3. Making work experience more impactful wirh better metrics and higher achivment levels.
        4. Improve the overall impression of experties, seniority and capabilities.
        5. Tailor the resume to better align with the job description provided.

        IMPORTANT RULES:
        - Keep the same basic career trjectory and eduction
        - Do not add any fictional jobs or degrees
        - Maintain the same job titles and employeers but enhance accomplishments
        - Focus particularly on the key factors identified from the job description.
        - The enhanced resume should be realisitc for someone with {self.difficulty_level}% more expertise.
        - Preserve the original format and structure of the resume. 
        """

        USER_PROMPT = f"""
        I need you to create a more competitive version of this candidate's resume.
        Candidate's Resume: {self.resume_text}
        Job Description: {self.job_description}
        Key Factors to focus enhancement on (these are the most important for the job) : {self.factors}
        Please create resume that is approximately {self.difficulty_level}% stronger than the original, focusing especially the ares related to key factors.
        Retun ONLY the enhanced resume with fixed header above and formated consistently with the original resume structure.
        """

        self.generated_resume = generate_llm_response(SYSTEM_PROMPT, USER_PROMPT)

        return self.generated_resume

    ### ATS Enhancement Methods ###
    def extract_ats_keywords(self, raw_text):
        if hasattr(self, "ats_keywords") and self.ats_keywords:
            return self.ats_keywords

        SYSTEM_PROMPT = """
        You are a ATS keyword engine. Convert the following raw job posting or resume text into exactly the JSON schema below:
        — Do not add any extra fields or prose.
        — Do not change the structure or key names; output only valid JSON matching the schema.
        - Do not format the response in Markdown or any other format. Just output raw JSON.
        
        Extract keywords EXACTLY as an ATS would index them.

        Output MUST be valid JSON:
        {
        "skills": [],
        "tools": [],
        "technologies": [],
        "methodologies": [],
        "certifications": [],
        "job_titles": []
        }

        Rules:
        - Use exact phrases from the job description
        - Include both acronym and expanded form if present
        - Do NOT infer or invent skills
        - Avoid soft skills
        """

        USER_PROMPT = f"""
        Job Description:
        {raw_text}
        Note: Please output only a valid JSON matching the EXACT schema with no surrounding commentary.
        """

        ats_keywords_raw = generate_llm_response(SYSTEM_PROMPT, USER_PROMPT, llm_type="openai_reasoning")
        ats_keywords = self.normalize_ats_keywords(self.parse_json_safe(ats_keywords_raw))
        return ats_keywords

    def generate_resume_ats_safe(self, resume_text=None):
        if self.generated_resume:
            return self.generated_resume

        if not hasattr(self, 'enhancement_descrition'):
            self.determine_enhancement()

        print("Normalized ATS Keywords:", self.ats_keywords)    
        print()
        factors = self.extract_factors()

        SYSTEM_PROMPT = f"""
        {self.RESUME_OUTPUT_CONTRACT}
        You are an ATS-safe resume enhancer AI specialist tasked with creating a stronger competitor version of candidate's resume.

        GOAL:
        Your job is to create a resume that is {self.enhancement_descrition} than the original (approximately {self.difficulty_level}% stronger) WITHOUT triggering ATS rejection :
        1. Enhance technical skills with {self.intensity} additions of relevant technologies and framworks.
        2. Updating project descriptions with more advanced concept and technical depth
        3. Making work experience more impactful wirh better metrics and higher achivment levels.
        4. Improve the overall impression of experties, seniority and capabilities.
        5. Tailor the resume to better align with the job description provided.
        
        ATS STRUCTURE (MANDATORY ORDER):
        SUMMARY
        SKILLS
        PROFESSIONAL EXPERIENCE
        PROJECTS
        EDUCATION
        CERTIFICATIONS (only if present)

        IMPORTANT RULES (STRICT):
        - Use standard section headers exactly as written
        - Skills must be listed as bullet or comma-separated lists
        - No tables, icons, emojis, columns, or special characters
        - Bullets must start with action verbs
        - Do not change job titles or employers
        - Keep the same basic career trjectory and eduction
        - Do not add any fictional jobs or degrees
        - Maintain the same job titles and employeers but enhance accomplishments
        - Focus particularly on the key factors identified from the job description.
        - The enhanced resume should be realisitc for someone with {self.difficulty_level}% more expertise.
        - Preserve the original format and structure of the resume. 

        KEYWORD COVERAGE REQUIREMENTS:
        - Every ATS keyword must appear at least once
        - Core skills must appear in BOTH SKILLS and EXPERIENCE
        - Do not repeat any keyword more than 2 times

        REALISM CONSTRAINTS:
        - Metric improvements ≤ 30%
        - Team sizes ≤ 15 unless explicitly senior
        - No new certifications unless implied in original resume
        - No more than +1 seniority level implied

        Focus enhancement especially on:
        {factors}

        ATS KEYWORDS:
        {self.ats_keywords}
        """

        USER_PROMPT = f"""
        Original Resume:
        {resume_text if resume_text else self.resume_text}

        Job Description:
        {self.job_description}

        Return ONLY the enhanced resume.
        Preserve original formatting and section layout.
        """

        self.generated_resume = generate_llm_response(SYSTEM_PROMPT, USER_PROMPT)
        return self.generated_resume


    def ats_regex_rule_pack(self, resume: str):
        issues = []

        # -------------------------------
        # 1. Unicode / non-ASCII bullets
        # -------------------------------
        if re.search(r"[•◆★▪➤✓✔]", resume):
            issues.append("Non-ATS Unicode bullet symbols detected")

        # -------------------------------
        # 2. Table / column layouts
        # -------------------------------
        if re.search(r"\t|\|", resume):
            issues.append("Possible table-based formatting detected")

        if resume.count("    ") > 20:
            issues.append("Possible multi-column layout detected")

        # -------------------------------
        # 3. Header validity
        # -------------------------------
        REQUIRED_HEADERS = [
            "SUMMARY",
            "SKILLS",
            "PROFESSIONAL EXPERIENCE",
            "EDUCATION"
        ]

        for header in REQUIRED_HEADERS:
            if header not in resume:
                issues.append(f"Missing required section header: {header}")

        # -------------------------------
        # 4. Metric overuse (LLM fingerprint)
        # -------------------------------
        percent_count = len(re.findall(r"%", resume))
        if percent_count > 8:
            issues.append("Excessive percentage-based metrics")

        # -------------------------------
        # 5. Suspicious metric patterns
        # -------------------------------
        if len(re.findall(r"increased .*?%", resume, re.IGNORECASE)) > 4:
            issues.append("Repeated metric phrasing detected")

        # -------------------------------
        # 6. Over-capitalization
        # -------------------------------
        if len(re.findall(r"\b[A-Z]{6,}\b", resume)) > 5:
            issues.append("Excessive capitalization may break parsing")

        # -------------------------------
        # 7. Date parsing issues
        # -------------------------------
        if re.search(r"\b(20\d{2})\s*-\s*(20\d{2})\b", resume):
            issues.append("Date ranges may not parse reliably")

        if re.search(r"\bPresent\b", resume, re.IGNORECASE):
            issues.append("Non-standard date token 'Present' detected")

        # -------------------------------
        # 8. Skill stuffing detection
        # -------------------------------
        skill_lines = re.findall(r"SKILLS(.+?)\n\n", resume, re.DOTALL)
        if skill_lines:
            skills = skill_lines[0].split(",")
            if len(skills) > 30:
                issues.append("Skill list too dense (possible keyword stuffing)")

        return issues

    def ats_score_resume(self, resume_text, job_description_keywords):
        ats_scorer = ATSScorer()
        ats_keywords_str= self.ats_keywords if self.ats_keywords else list(self.normalize_ats_keywords(
                self.parse_json_safe(
                    self.extract_ats_keywords()
                )
            ).values())
        final_score = ats_scorer.final_ats_score(
            resume=resume_text,
            job_description=job_description_keywords,
            ats_keywords=ats_keywords_str,
            embed_fn=generate_embedding
        )

        return final_score

    def semantic_gap_terms(self, resume_text, jd_text, embed_fn, top_k=8):
        """
        Extract JD phrases that are semantically distant from the resume.
        """
        jd_sentences = [
            s.strip() for s in re.split(r"[.\n]", jd_text) if len(s.strip()) > 20
        ]

        resume_emb = embed_fn(resume_text)
        gaps = []

        for sent in jd_sentences:
            sent_emb = embed_fn(sent)
            sim = cosine_similarity([resume_emb], [sent_emb])[0][0]
            gaps.append((sim, sent))

        gaps.sort(key=lambda x: x[0])
        return [g[1] for g in gaps[:top_k]]


    def generate_ats_optimized_resume(self, min_score=85, max_attempts=3):
        import json
        resume = self.generate_resume_ats_safe()
        
        regex_issues = self.ats_regex_rule_pack(resume)
        print("ATS Regex Issues Detected:", regex_issues)
        if regex_issues:
            resume = self.improve_resume_fixed_ats_issues(regex_issues, resume, min_score)

        job_description_keywords_list = self.flatten_keywords_str(self.ats_keywords)
        job_description_keywords = ", ".join(job_description_keywords_list)
        print("Job Description Keywords for ATS Optimization:", job_description_keywords_list)

        generate_recommendation = self.skill_comparison.generate_skill_comparison()

        semantic_score = []
        for attempt in range(max_attempts):
            score_report_str = self.ats_score_resume(resume, job_description_keywords)
            print()
            print(f"ATS Scoring Attempt {attempt+1}: {score_report_str}")
            print()
            
            score_report = self.parse_json_safe(score_report_str)            
                        
            if score_report.get("final_score", 0) >= min_score:
                return resume, generate_recommendation

            semantic_score.append(score_report.get("semantic_score", 0))
            if attempt > 0:
                # If semantic score is not improving, break early
                if semantic_score[-1] - semantic_score[-2] < 0.02:
                    print("Semantic score not improving, stopping attempts.")
                    print()
                    return resume, generate_recommendation


            semantic_gaps = self.semantic_gap_terms(
                resume,
                job_description_keywords,
                generate_embedding
            )

            print("Semantic Gaps Identified:", semantic_gaps)
            print()

            SYSTEM_PROMPT = f"""
            {self.RESUME_OUTPUT_CONTRACT}

            You are an ATS resume improvement engine.

            TARGETED GOAL:
            Increase semantic alignment with the job description.

            SEMANTIC GAPS (concepts missing or weakly represented):
            {semantic_gaps}

            RULES:
            For each semantic gap:
                - Insert at least ONE verbatim phrase (≥4 consecutive words)
                - Place it inside an existing PROFESSIONAL EXPERIENCE bullet
                - Do not paraphrase the phrase
            ADDITIONAL CONSTRAINTS:
            - Do NOT add new roles or employers
            - Do NOT repeat any keyword more than twice
            - Prefer PROFESSIONAL EXPERIENCE over SUMMARY
            - Preserve ATS-safe formatting
            - Return ONLY the resume
            """

            resume = generate_llm_response(SYSTEM_PROMPT, resume)
            #resume = self.generate_resume_ats_safe(resume)

        return resume, generate_recommendation

    def improve_resume_fixed_ats_issues(self, regex_issue, resume, min_score=85):
        SYSTEM_PROMPT = f"""
        {self.RESUME_OUTPUT_CONTRACT}
        You are an ATS resume improvement engine.
        Fix all regex-detected ATS issues.
        Regex Issues:
        {regex_issue}
        Ensure the resume scores at least {min_score} on ATS evaluation.
        Do not add commentary.
        """

        regex_fix_resume = generate_llm_response(SYSTEM_PROMPT, resume)
        return regex_fix_resume

    def normalize_ats_keywords(self, ats_keywords):
        normalized = {}
        for group, keywords in ats_keywords.items():
            normalized[group] = []
            for kw in keywords:
                kw = kw.strip()
                if len(kw.split()) <= 4:   # atomic only
                    normalized[group].append(kw)
        return normalized    

    def flatten_keywords_str(self, grouped_keywords):
        flat = []
        for group in grouped_keywords.values():
            flat.extend(group)
        keyword_list = list(set(flat))
        #return ", ".join(keyword_list)
        return keyword_list
    
    def parse_json_safe(self, json_string):
        import json
        
        # If already a dict, return it
        if isinstance(json_string, dict):
            return json_string
        
        # If it's a string, try to parse it
        if isinstance(json_string, str):
            try:
                data = json.loads(json_string)
                return data
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                return {}
        
        # For any other type, return empty dict
        return {}


if __name__ == "__main__":
    ai_competitor = AICompetitor(resume, jd, 30)
    factors = ai_competitor.extract_factors()
    print("Extracted Factors:", factors)
    print()
    enhanced_resume = ai_competitor.generate_resume()
    print("Generated Enhanced Resume:", enhanced_resume)



    

