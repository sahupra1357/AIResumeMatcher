# AI Resume Matcher

An AI-powered resume optimization tool that analyzes job descriptions and enhances resumes to improve ATS (Applicant Tracking System) compatibility and match scores.

## Features

- **Resume Enhancement**: Generate competitive resumes optimized for specific job descriptions
- **ATS Optimization**: Create ATS-safe resumes with keyword optimization
- **Semantic Analysis**: Use embeddings and semantic similarity for intelligent matching
- **Multi-LLM Support**: Supports multiple AI providers (OpenAI, Claude, Google, DeepSeek, Groq)
- **Progress Tracking**: Real-time progress bars for LLM operations
- **Observability**: Built-in monitoring with Arize Phoenix

## Project Structure

```
backend/
├── core/
│   └── model.py           # LLM integration and model operations
├── data/
│   └── input.py           # Resume and job description inputs
├── resume_match/
│   ├── generate_ai_competitor.py  # Main AI resume generator
│   ├── ats_scorer.py      # ATS scoring logic
│   └── observability.py   # Monitoring setup
├── output/                # Generated resumes
├── main.py               # Entry point
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
# Extract ATS keywords
ats_keywords = ai_competitor.extract_ats_keywords()

# Generate ATS-optimized resume
ats_optimized_resume = ai_competitor.generate_ats_optimized_resume()
```

### Run the Application

```bash
# Run ATS optimization
python main.py

# Or customize in main.py
python -c "from main import main; main()"
```

## API Reference

### AICompetitor Class

#### Methods

- **`extract_factors()`**: Extracts 5 key factors from job description
- **`extract_ats_keywords()`**: Identifies ATS-friendly keywords
- **`generate_resume()`**: Creates enhanced resume
- **`generate_resume_ats_safe()`**: Generates ATS-optimized resume
- **`generate_ats_optimized_resume()`**: Creates fully optimized resume with scoring
- **`ats_score_resume(resume_text)`**: Scores resume against ATS criteria

### Supported LLM Types

- `openai` - GPT models
- `openai_reasoning` - OpenAI reasoning models (o1-mini, etc.)
- `claude` - Anthropic Claude
- `google` - Google Gemini
- `deepseek` - DeepSeek models
- `groq` - Groq inference

## Features in Detail

### Progress Bars
All LLM calls display real-time progress indicators with elapsed time and calling context.

### ATS Scoring
The system scores resumes on multiple criteria:
- Contact information completeness
- Keyword matching
- Format compliance
- Experience relevance
- Skills alignment

### Semantic Matching
Uses embeddings to calculate semantic similarity between resume and job description for intelligent optimization.

## Development

### Running Tests

```bash
python backend/data/test2.py
python backend/data/test3.py
```

### Output

Generated resumes are saved in `backend/output/` with timestamps.

## Dependencies

Key dependencies:
- `openai>=2.7.1` - OpenAI API
- `anthropic>=0.72.0` - Claude API
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

### File Not Found Errors
The `output/` directory is created automatically. If you get file errors, ensure write permissions.

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