import { useState } from 'react';
import { analyzeResume } from './services/api';
import UploadSection from './components/UploadSection';
import ResultsSection from './components/ResultsSection';
import EnhancedResume from './components/EnhancedResume';
import { Loader2, FileCheck } from 'lucide-react';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResumeFile(file);
      setFileName(file.name);
      setError('');
    }
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setError('Please upload a resume file');
      return;
    }

    if (!jobDescription || jobDescription.trim().length < 50) {
      setError('Please provide a detailed job description (at least 50 characters)');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const analysisResults = await analyzeResume(resumeFile, jobDescription);
      setResults(analysisResults);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setFileName('');
    setJobDescription('');
    setResults(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <FileCheck className="w-12 h-12 text-primary-600" />
            <h1 className="text-4xl font-bold text-gray-900">ATS Resume Matcher</h1>
          </div>
          <p className="text-lg text-gray-600">
            Analyze your resume against job descriptions and get AI-powered recommendations
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Upload Section */}
          <div>
            <UploadSection
              onFileChange={handleFileChange}
              onJobDescriptionChange={handleJobDescriptionChange}
              fileName={fileName}
              jobDescription={jobDescription}
            />

            {/* Action Buttons */}
            <div className="flex gap-4 mt-6">
              <button
                onClick={handleAnalyze}
                disabled={loading || !resumeFile || !jobDescription}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  'Analyze Resume'
                )}
              </button>
              <button
                onClick={handleReset}
                disabled={loading}
                className="btn-secondary"
              >
                Reset
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800">{error}</p>
              </div>
            )}

            {/* Info Box */}
            <div className="card mt-6 bg-blue-50 border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-2">How it works:</h3>
              <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
                <li>Upload your resume (PDF or DOCX format)</li>
                <li>Paste the complete job description</li>
                <li>Click "Analyze Resume" to get instant feedback</li>
                <li>Review ATS score, missing skills, and improvement suggestions</li>
                <li>Get an AI-enhanced resume optimized for the job</li>
              </ol>
            </div>
          </div>

          {/* Right Column - Results Section */}
          <div>
            {loading && (
              <div className="card flex flex-col items-center justify-center py-12">
                <Loader2 className="w-16 h-16 text-primary-600 animate-spin mb-4" />
                <p className="text-lg font-medium text-gray-700">Analyzing your resume...</p>
                <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
              </div>
            )}

            {!loading && !results && !error && (
              <div className="card flex flex-col items-center justify-center py-12 text-center">
                <FileCheck className="w-16 h-16 text-gray-400 mb-4" />
                <p className="text-lg font-medium text-gray-600">No results yet</p>
                <p className="text-sm text-gray-500 mt-2">
                  Upload your resume and job description to get started
                </p>
              </div>
            )}

            {results && <ResultsSection results={results} />}
          </div>
        </div>

        {/* Enhanced Resume Section - Full Width Below */}
        {results && results.enhanced_resume && (
          <div className="mt-8">
            <EnhancedResume results={results} />
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-600 text-sm">
          <p>Powered by OpenAI GPT-4 | Built with React & FastAPI</p>
        </div>
      </div>
    </div>
  );
}

export default App;
