import os
from openai import OpenAI
from typing import Dict, List
import json
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add services directory to path to import AICompetitor
sys.path.append(str(Path(__file__).parent))

load_dotenv()


class ATSMatcher:
    """Service to match resume with job description using OpenAI"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    def analyze_match(self, resume_text: str, job_description: str, difficulty_level: int = 30) -> Dict:
        """
        Analyze resume against job description and return comprehensive matching results
        including enhanced resume generation using AICompetitor logic

        Args:
            resume_text: The resume text to analyze
            job_description: The job description to match against
            difficulty_level: Enhancement level for resume generation (0-100, default 30)

        Returns:
            Dict containing analysis results and enhanced resume
        """
        # Import AICompetitor here to avoid circular imports
        from app.services.generate_ai_competitor import AICompetitor

        # Create AICompetitor instance with the provided difficulty level
        ai_competitor = AICompetitor(resume_text, job_description, difficulty_level)

        try:
            # Generate enhanced resume using the complete AICompetitor pipeline
            enhanced_resume, skill_recommendations = ai_competitor.generate_ats_optimized_resume(
                min_score=85,
                max_attempts=3
            )

            # Get the ATS score for the enhanced resume
            ats_keywords_list = ai_competitor.flatten_keywords_str(ai_competitor.ats_keywords)
            ats_keywords_str = ", ".join(ats_keywords_list)
            ats_score_report = ai_competitor.ats_score_resume(enhanced_resume, ats_keywords_str)

            # Parse the ATS score
            try:
                ats_score_data = ai_competitor.parse_json_safe(ats_score_report)
                final_ats_score = ats_score_data.get("final_score", 0)
            except:
                final_ats_score = 0

            # Generate basic analysis using OpenAI for missing skills and suggestions
            prompt = self._create_analysis_prompt(resume_text, job_description)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS (Applicant Tracking System) analyzer and resume consultant. Provide detailed, actionable feedback in valid JSON format only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            # Add enhanced resume and related data to the result
            result["enhanced_resume"] = enhanced_resume
            result["skill_comparison"] = skill_recommendations
            result["enhanced_ats_score"] = final_ats_score
            result["ats_keywords"] = ai_competitor.ats_keywords
            result["key_factors"] = ai_competitor.extract_factors()

            return result

        except Exception as e:
            raise Exception(f"Analysis error: {str(e)}")

    def _create_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Create detailed prompt for OpenAI analysis"""
        return f"""
Analyze the following resume against the job description and provide a comprehensive ATS compliance report.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide your analysis in the following JSON format:
{{
    "ats_score": <float between 0-100>,
    "missing_skills": [
        {{
            "skill": "<skill name>",
            "category": "<Technical|Soft Skill|Certification|Experience>",
            "importance": "<Critical|Important|Nice to have>"
        }}
    ],
    "matched_skills": ["<skill1>", "<skill2>", ...],
    "keyword_suggestions": [
        {{
            "keyword": "<keyword or phrase>",
            "context": "<where to add it>",
            "reason": "<why it's important for ATS>"
        }}
    ],
    "resume_improvements": [
        {{
            "section": "<section name: Summary|Experience|Skills|Education>",
            "current_content": "<brief excerpt or 'Missing'>",
            "suggested_content": "<improved version>",
            "improvements": ["<improvement point 1>", "<improvement point 2>"]
        }}
    ],
    "overall_feedback": "<2-3 sentences of actionable advice>",
    "match_summary": {{
        "experience_match": "<percentage or assessment>",
        "skills_match": "<percentage or assessment>",
        "education_match": "<percentage or assessment>",
        "key_strengths": ["<strength 1>", "<strength 2>"],
        "critical_gaps": ["<gap 1>", "<gap 2>"]
    }}
}}

Guidelines:
1. ATS Score Calculation:
   - Consider keyword matching, skills alignment, experience relevance, and formatting
   - Be realistic but constructive

2. Missing Skills:
   - Only list skills explicitly mentioned in JD but missing from resume
   - Categorize by type and importance

3. Keyword Suggestions:
   - Focus on ATS-friendly terms from the job description
   - Suggest natural placement contexts

4. Resume Improvements:
   - Provide specific, actionable suggestions for each section
   - Include exact wording when possible
   - Focus on ATS optimization while maintaining readability

5. Match Summary:
   - Provide percentage or qualitative assessment for each area
   - Highlight both strengths and gaps

Return ONLY valid JSON, no additional text.
"""
