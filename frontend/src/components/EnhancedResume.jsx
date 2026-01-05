import { FileText, Download, Copy, Check, Sparkles, TrendingUp } from 'lucide-react';
import { useState } from 'react';

export default function EnhancedResume({ results }) {
  const [copied, setCopied] = useState(false);

  if (!results || !results.enhanced_resume) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(results.enhanced_resume);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([results.enhanced_resume], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'enhanced_resume.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* Enhanced Resume Header */}
      <div className="card bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Sparkles className="w-8 h-8 text-purple-600" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">AI-Enhanced Resume</h2>
              <p className="text-sm text-gray-600">Optimized for ATS and job requirements</p>
            </div>
          </div>

          {results.enhanced_ats_score && (
            <div className="text-right">
              <div className={`text-3xl font-bold ${getScoreColor(results.enhanced_ats_score)}`}>
                {results.enhanced_ats_score.toFixed(1)}%
              </div>
              <p className="text-xs text-gray-600">Enhanced Score</p>
            </div>
          )}
        </div>

        {/* Score Comparison */}
        {results.enhanced_ats_score && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="font-medium text-gray-700">Original Score</span>
              <span className={`font-bold ${getScoreColor(results.ats_score)}`}>
                {results.ats_score.toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="font-medium text-gray-700">Enhanced Score</span>
              <span className={`font-bold ${getScoreColor(results.enhanced_ats_score)}`}>
                {results.enhanced_ats_score.toFixed(1)}%
              </span>
            </div>
            <div className="flex items-center gap-2 mt-3">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <span className="text-sm font-semibold text-green-700">
                +{(results.enhanced_ats_score - results.ats_score).toFixed(1)}% improvement
              </span>
            </div>
          </div>
        )}

        {/* Key Factors */}
        {results.key_factors && (
          <div className="mb-4 p-3 bg-white rounded-lg border border-purple-200">
            <h3 className="text-sm font-semibold text-purple-900 mb-2">Key Focus Areas</h3>
            <p className="text-sm text-gray-700 whitespace-pre-wrap">{results.key_factors}</p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy Resume
              </>
            )}
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
          >
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </div>

      {/* Enhanced Resume Content */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-gray-600" />
          <h3 className="text-xl font-semibold text-gray-900">Enhanced Resume Content</h3>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 max-h-[600px] overflow-y-auto">
          <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800 leading-relaxed">
            {results.enhanced_resume}
          </pre>
        </div>
      </div>

      {/* Skill Comparison */}
      {results.skill_comparison && (
        <div className="card">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            Skill Enhancement Summary
          </h3>
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800 leading-relaxed">
              {results.skill_comparison}
            </pre>
          </div>
        </div>
      )}

      {/* ATS Keywords */}
      {results.ats_keywords && (
        <div className="card">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">ATS Keywords Included</h3>
          <div className="space-y-4">
            {Object.entries(results.ats_keywords).map(([category, keywords]) => (
              keywords.length > 0 && (
                <div key={category}>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2 capitalize">
                    {category.replace('_', ' ')}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {keywords.map((keyword, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-xs font-medium"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
