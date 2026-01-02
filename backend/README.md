# AI Resume Matcher

An AI-powered resume optimization tool that analyzes job descriptions and enhances resumes to improve ATS (Applicant Tracking System) compatibility and match scores.

## Features

- **Resume Enhancement**: Generate competitive resumes optimized for specific job descriptions
- **ATS Optimization**: Create ATS-safe resumes with keyword optimization and recommendations
- **PDF Generation**: Automatically converts text output to properly formatted PDF files
- **Semantic Analysis**: Use embeddings and semantic similarity for intelligent matching
- **Multi-LLM Support**: Supports multiple AI providers (OpenAI, Claude, Google, DeepSeek, Groq)
- **Progress Tracking**: Real-time progress bars for both application flow and LLM operations
- **Execution Timing**: Tracks and displays total time taken for resume generation
- **Observability**: Built-in monitoring with Arize Phoenix
- **Automated Output**: Automatically saves optimized resumes and recommendations as PDFs with timestamps

## Project Structure

```
backend/
├── core/
│   └── model.py           # LLM integration with progress bars
├── data/
│   ├── input.py           # Resume and job description inputs
│   ├── test2.py           # Keyword flattening tests
│   └── test3.py           # LLM integration tests
├── resume_match/
│   ├── generate_ai_competitor.py  # Main AI resume generator
│   ├── enhance_resume.py  # Resume enhancement utilities
│   ├── ats_scorer.py      # ATS scoring logic
│   └── observability.py   # Monitoring setup
├── output/                # Generated resumes and recommendations
├── main.py               # Entry point with progress tracking
└── pyproject.toml        # Dependencies
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/sahupra1357/AIResumeMatcher.git
cd AIResumeMatcher/backend
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```bash
pip install -e .
# or with uv
uv pip install -e .
```

## Configuration

Create a `.env` file in the `backend/` directory with your API keys:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_REASONING_MODEL=o1-mini
OPENAI_AUDIO_MODEL=whisper-1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Anthropic Claude (optional)
ANTHROPIC_API_KEY=your_claude_api_key
CLAUDE_MODEL=claude-3-sonnet-20240229

# Google (optional)
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=gemini-2.0-flash

# DeepSeek (optional)
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_MODEL=deepseek-chat

# Groq (optional)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-70b-versatile
```

## Usage

### Basic Resume Enhancement

```python
from resume_match.generate_ai_competitor import AICompetitor
from data.input import resume, jd

# Initialize with resume text, job description, and difficulty level
ai_competitor = AICompetitor(resume, jd, difficulty_level=30)

# Extract key factors from job description
factors = ai_competitor.extract_factors()

# Generate enhanced resume
enhanced_resume = ai_competitor.generate_resume()
```

### ATS-Optimized Resume

```python
# Generate ATS-optimized resume with recommendations
ats_optimized_resume, recommendations = ai_competitor.generate_ats_optimized_resume()

# The method returns both the optimized resume and improvement recommendations
print("Optimized Resume:", ats_optimized_resume)
print("Recommendations:", recommendations)
```

### Run the Application

```bash
# Run ATS optimization (default)
python main.py

# Or run basic resume enhancement
python -c "from main import main; main()"
```

**Output:**
- The application displays real-time progress bars with emoji indicators
- Shows total execution time upon completion
- Automatically converts text to PDF format with proper formatting (headers, bullets, paragraphs)
- Saves two PDF files in `backend/output/`:
  - `ats_optimized_resume_{timestamp}.pdf` - The optimized resume in PDF format
  - `ats_recommendations_{timestamp}.pdf` - Improvement recommendations in PDF format

**Example Output:**
```
Hello from backend ATS!
🎯 ATS Optimization: 100%|████████████████| 100/100
✅ Files saved:
   📄 Resume: ./backend/output/ats_optimized_resume_20260102_143022.pdf
   📋 Recommendations: ./backend/output/ats_recommendations_20260102_143022.pdf
⏱️  Total Time Taken: 45.32 seconds
```

## API Reference

### AICompetitor Class

#### Methods

- **`extract_factors()`**: Extracts 5 key factors from job description
- **`extract_ats_keywords()`**: Identifies ATS-friendly keywords grouped by category
- **`generate_resume()`**: Creates enhanced resume with progress tracking
- **`generate_resume_ats_safe()`**: Generates ATS-optimized resume
- **`generate_ats_optimized_resume(min_score=85, max_attempts=3)`**: Creates fully optimized resume with scoring and recommendations
  - Returns: `(resume_text, recommendations)`
  - Iteratively improves resume until min_score is reached or max_attempts exhausted
- **`ats_score_resume(resume_text, keywords)`**: Scores resume against ATS criteria
- **`flatten_keywords_str(keywords_dict)`**: Flattens grouped keywords into a list

### Supported LLM Types

- `openai` - GPT models
- `openai_reasoning` - OpenAI reasoning models (o1-mini, etc.)
- `claude` - Anthropic Claude
- `google` - Google Gemini
- `deepseek` - DeepSeek models
- `groq` - Groq inference

## Features in Detail

### Progress Bars

The application features two levels of progress tracking:

1. **Application-level progress** (main.py):
   - 🔧 Initialization phase
   - 🔍 Factor extraction
   - ✨ Resume generation
   - 💾 File saving
   - ⏱️  Total execution time display

2. **LLM-level progress** (model.py):
   - Individual progress bars for each LLM API call
   - Shows calling method name and LLM type
   - Displays elapsed time per call
   - Updates at key processing points

**Example:**
```
🎯 ATS Optimization: 10%|██░░░░░░░░░░░░░░| Initializing...
🤖 openai_reasoning (extract_ats_keywords): 70%|███████░░░| 0:00:03
```

### ATS Scoring
The system scores resumes on multiple criteria:
- Contact information completeness
- Keyword matching with semantic analysis
- Format compliance and ATS-safe structure
- Experience relevance to job description
- Skills alignment and gap identification
- Iterative improvement until target score reached

### Semantic Matching
Uses embeddings to calculate semantic similarity between resume and job description for intelligent optimization.

## Development

### Running Tests

```bash
python backend/data/test2.py
python backend/data/test3.py
```

### Output

Generated files are automatically saved in `backend/output/` with timestamps:
- **Optimized Resumes**: `ats_optimized_resume_{timestamp}.pdf` - Properly formatted PDF documents
- **Recommendations**: `ats_recommendations_{timestamp}.pdf` - PDF with improvement suggestions

**PDF Features:**
- Automatic text-to-PDF conversion using FPDF2
- Formatted headers (markdown # headers and ALL CAPS)
- Bullet point formatting (•)
- Proper page breaks and margins
- Handles long text gracefully
- Opens in any PDF viewer (Preview, Adobe, etc.)

The application displays:
- Real-time progress for each operation
- Saved file paths upon completion
- Total execution time in seconds

## Dependencies

Key dependencies:
- `openai>=2.7.1` - OpenAI API
- `anthropic>=0.72.0` - Claude API
- `fpdf2>=2.7.0` - PDF generation
- `markdown>=3.5.0` - Markdown processing
- `tqdm>=4.66.0` - Progress bars
- `arize-phoenix>=12.27.0` - Observability
- `scikit-learn` - Semantic similarity
- `numpy` - Numerical operations

See [pyproject.toml](pyproject.toml) for complete list.

## Troubleshooting

### Invalid API Key
If you get authentication errors, verify your `.env` file has valid API keys:
```bash
cat backend/.env
```

### Module Import Errors
Ensure you're running from the project root and the virtual environment is activated:
```bash
cd /path/to/AIResumeMatcher
source backend/.venv/bin/activate
python backend/main.py
```

### PDF Generation Errors
If you encounter "Not enough horizontal space" errors:
- The application automatically handles long text by breaking it into chunks
- Very long lines are split intelligently
- Problematic lines are skipped gracefully

If PDFs don't render properly:
```bash
# Reinstall PDF dependencies
uv pip install --force-reinstall fpdf2 markdown
```

### PDF Files Won't Open
Ensure you have the latest version of FPDF2:
```bash
uv pip install --upgrade fpdf2
```
The generated PDFs are standard PDF/A format compatible with all viewers.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is private. Contact the repository owner for licensing information.

## Contact

Repository Owner: [@sahupra1357](https://github.com/sahupra1357)

---

**Note**: Keep your `.env` file secure and never commit it to version control. The `.gitignore` is configured to exclude it automatically.