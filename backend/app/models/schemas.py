from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AnalysisRequest(BaseModel):
    job_description: str = Field(..., description="The job description text")
    resume_text: str = Field(..., description="The extracted resume text")


class MissingSkill(BaseModel):
    skill: str
    category: str  # e.g., "Technical", "Soft Skill", "Certification"
    importance: str  # "Critical", "Important", "Nice to have"


class KeywordSuggestion(BaseModel):
    keyword: str
    context: str
    reason: str


class ResumeSection(BaseModel):
    section: str  # e.g., "Summary", "Experience", "Skills"
    current_content: str
    suggested_content: str
    improvements: List[str]


class AnalysisResponse(BaseModel):
    ats_score: float = Field(..., ge=0, le=100, description="ATS matching score (0-100)")
    missing_skills: List[MissingSkill]
    keyword_suggestions: List[KeywordSuggestion]
    matched_skills: List[str]
    resume_improvements: List[ResumeSection]
    overall_feedback: str
    match_summary: Dict[str, Any]
    enhanced_resume: Optional[str] = Field(None, description="AI-generated enhanced resume")
    skill_comparison: Optional[str] = Field(None, description="Skill comparison recommendations")
    enhanced_ats_score: Optional[float] = Field(None, description="ATS score for enhanced resume")
    ats_keywords: Optional[Dict[str, List[str]]] = Field(None, description="Extracted ATS keywords")
    key_factors: Optional[str] = Field(None, description="Key factors from job description")


class HealthResponse(BaseModel):
    status: str
    message: str
