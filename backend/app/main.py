from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ATS Resume Matcher API",
    description="API for analyzing resumes against job descriptions with ATS compliance scoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "*")

# Parse origins and strip whitespace
if ALLOWED_ORIGINS_STR == "*":
    ALLOWED_ORIGINS = ["*"]
    ALLOW_ORIGIN_REGEX = None
else:
    # Split by comma and strip whitespace from each origin
    origins_list = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",")]

    # Separate wildcard patterns from explicit origins
    explicit_origins = [o for o in origins_list if "*" not in o]
    wildcard_patterns = [o for o in origins_list if "*" in o]

    # Convert wildcard patterns to regex
    if wildcard_patterns:
        # Convert patterns like https://*.vercel.app to regex
        regex_patterns = []
        for pattern in wildcard_patterns:
            # Escape dots and convert * to regex pattern
            regex_pattern = pattern.replace(".", r"\.").replace("*", r"[a-zA-Z0-9\-]+")
            regex_patterns.append(regex_pattern)
        ALLOW_ORIGIN_REGEX = "|".join(regex_patterns)
    else:
        ALLOW_ORIGIN_REGEX = None

    ALLOWED_ORIGINS = explicit_origins if explicit_origins else ["*"]

logger.info(f"CORS Configuration:")
logger.info(f"  Allowed Origins: {ALLOWED_ORIGINS}")
logger.info(f"  Origin Regex: {ALLOW_ORIGIN_REGEX}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["ATS Analysis"])


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting ATS Resume Matcher API")

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("⚠️  OPENAI_API_KEY not found in environment variables!")
        logger.warning("Please set your OpenAI API key in the .env file")
    else:
        logger.info("✓ OpenAI API key configured")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down ATS Resume Matcher API")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ATS Resume Matcher API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
