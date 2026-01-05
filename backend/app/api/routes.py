from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import AnalysisResponse, HealthResponse, MissingSkill, KeywordSuggestion, ResumeSection
from app.services.resume_parser import ResumeParser
from app.services.matcher import ATSMatcher
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
resume_parser = ResumeParser()
ats_matcher = ATSMatcher()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="ATS Resume Matcher API is running"
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze resume against job description

    Parameters:
    - resume: Resume file (PDF or DOCX format)
    - job_description: Job description text

    Returns:
    - Comprehensive ATS analysis including score, missing skills, and suggestions
    """
    try:
        # Validate file type
        if not resume.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        allowed_extensions = ['.pdf', '.docx']
        file_ext = '.' + resume.filename.split('.')[-1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
            )

        # Read file content
        file_content = await resume.read()

        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Parse resume
        logger.info(f"Parsing resume: {resume.filename}")
        resume_text = resume_parser.parse_resume(file_content, resume.filename)
        resume_text = resume_parser.clean_text(resume_text)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume. Please ensure the file is not corrupted."
            )

        # Validate job description
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description is too short. Please provide a detailed job description."
            )

        # Perform ATS analysis
        logger.info("Performing ATS analysis")
        analysis_result = ats_matcher.analyze_match(resume_text, job_description)

        # Convert to response model
        response = AnalysisResponse(
            ats_score=float(analysis_result.get("ats_score", 0)),
            missing_skills=[
                MissingSkill(**skill) for skill in analysis_result.get("missing_skills", [])
            ],
            keyword_suggestions=[
                KeywordSuggestion(**kw) for kw in analysis_result.get("keyword_suggestions", [])
            ],
            matched_skills=analysis_result.get("matched_skills", []),
            resume_improvements=[
                ResumeSection(**section) for section in analysis_result.get("resume_improvements", [])
            ],
            overall_feedback=analysis_result.get("overall_feedback", ""),
            match_summary=analysis_result.get("match_summary", {}),
            enhanced_resume=analysis_result.get("enhanced_resume"),
            skill_comparison=analysis_result.get("skill_comparison"),
            enhanced_ats_score=analysis_result.get("enhanced_ats_score"),
            ats_keywords=analysis_result.get("ats_keywords"),
            key_factors=analysis_result.get("key_factors")
        )

        logger.info(f"Analysis completed. ATS Score: {response.ats_score}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during analysis: {str(e)}"
        )
