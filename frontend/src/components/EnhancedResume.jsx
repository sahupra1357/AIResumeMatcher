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
    <div className="space-y-4">
      {/* Enhanced Resume Header - Compact */}
      <div className="card bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-200">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-600" />
            <div>
              <h2 className="text-lg font-bold text-gray-900">AI-Enhanced Resume</h2>
              <p className="text-xs text-gray-600">Optimized for ATS</p>
            </div>
          </div>

          {results.enhanced_ats_score && (
            <div className="text-right">
              <div className={`text-2xl font-bold ${getScoreColor(results.enhanced_ats_score)}`}>
                {results.enhanced_ats_score.toFixed(1)}%
              </div>
              <div className="flex items-center gap-1 text-xs text-green-700">
                <TrendingUp className="w-3 h-3" />
                <span>+{(results.enhanced_ats_score - results.ats_score).toFixed(1)}%</span>
              </div>
            </div>
          )}
        </div>

        {/* Key Factors - Compact */}
        {results.key_factors && (
          <div className="mb-3 p-2 bg-white rounded-lg border border-purple-200">
            <h3 className="text-xs font-semibold text-purple-900 mb-1">Key Focus Areas</h3>
            <p className="text-xs text-gray-700 line-clamp-2" title={results.key_factors}>
              {results.key_factors}
            </p>
          </div>
        )}

        {/* Action Buttons - Compact */}
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-3 py-1.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-xs font-medium"
          >
            {copied ? (
              <>
                <Check className="w-3 h-3" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" />
                Copy
              </>
            )}
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center gap-1 px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-xs font-medium"
          >
            <Download className="w-3 h-3" />
            Download
          </button>
        </div>
      </div>

      {/* Enhanced Resume Content */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-gray-600" />
            <h3 className="text-xl font-semibold text-gray-900">Enhanced Resume</h3>
          </div>
          <button
            onClick={handleCopy}
            className="text-sm px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors flex items-center gap-1"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                <span>Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>

        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 max-h-[500px] overflow-y-auto">
          <pre className="whitespace-pre-wrap font-sans text-xs text-gray-800 leading-relaxed">
            {results.enhanced_resume}
          </pre>
        </div>
      </div>

      {/* Skill Comparison - Compact */}
      {results.skill_comparison && (
        <div className="card">
          <h3 className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-blue-600" />
            Skill Enhancement Summary
          </h3>
          <div className="bg-blue-50 rounded-lg p-3 border border-blue-200 max-h-[200px] overflow-y-auto">
            <pre className="whitespace-pre-wrap font-sans text-xs text-gray-800 leading-relaxed">
              {results.skill_comparison}
            </pre>
          </div>
        </div>
      )}

      {/* ATS Keywords - Compact & Collapsible */}
      {results.ats_keywords && (
        <details className="card cursor-pointer" open>
          <summary className="text-sm font-semibold text-gray-900 mb-3 list-none flex items-center justify-between hover:text-purple-600">
            <span>ATS Keywords Included</span>
            <span className="text-xs text-gray-500">Click to expand/collapse</span>
          </summary>
          <div className="space-y-3 pt-2">
            {Object.entries(results.ats_keywords).map(([category, keywords]) => (
              keywords.length > 0 && (
                <div key={category}>
                  <h4 className="text-xs font-semibold text-gray-700 mb-1.5 capitalize">
                    {category.replace('_', ' ')} ({keywords.length})
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {keywords.slice(0, 10).map((keyword, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-indigo-100 text-indigo-800 rounded-full text-xs font-medium"
                      >
                        {keyword}
                      </span>
                    ))}
                    {keywords.length > 10 && (
                      <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs">
                        +{keywords.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              )
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
