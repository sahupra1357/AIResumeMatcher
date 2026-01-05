import { CheckCircle, XCircle, AlertCircle, TrendingUp, Award, Lightbulb } from 'lucide-react';

export default function ResultsSection({ results }) {
  if (!results) return null;

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

  const getImportanceColor = (importance) => {
    switch (importance.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-800';
      case 'important':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* ATS Score */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Award className="w-6 h-6" />
            ATS Match Score
          </h2>
          <div className={`text-5xl font-bold ${getScoreColor(results.ats_score)}`}>
            {results.ats_score.toFixed(1)}%
          </div>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className={`h-4 rounded-full transition-all ${getScoreBgColor(results.ats_score)}`}
            style={{ width: `${results.ats_score}%` }}
          />
        </div>
        <p className="text-gray-700">{results.overall_feedback}</p>
      </div>

      {/* Match Summary */}
      {results.match_summary && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Match Summary
          </h2>
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Experience Match</p>
              <p className="text-lg font-semibold">{results.match_summary.experience_match}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Skills Match</p>
              <p className="text-lg font-semibold">{results.match_summary.skills_match}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Education Match</p>
              <p className="text-lg font-semibold">{results.match_summary.education_match}</p>
            </div>
          </div>
          {results.match_summary.key_strengths?.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-semibold text-green-700 mb-2">Key Strengths:</p>
              <ul className="list-disc list-inside space-y-1">
                {results.match_summary.key_strengths.map((strength, idx) => (
                  <li key={idx} className="text-sm text-gray-700">{strength}</li>
                ))}
              </ul>
            </div>
          )}
          {results.match_summary.critical_gaps?.length > 0 && (
            <div>
              <p className="text-sm font-semibold text-red-700 mb-2">Critical Gaps:</p>
              <ul className="list-disc list-inside space-y-1">
                {results.match_summary.critical_gaps.map((gap, idx) => (
                  <li key={idx} className="text-sm text-gray-700">{gap}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Matched Skills */}
      {results.matched_skills?.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            Matched Skills ({results.matched_skills.length})
          </h2>
          <div className="flex flex-wrap gap-2">
            {results.matched_skills.map((skill, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Skills */}
      {results.missing_skills?.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <XCircle className="w-5 h-5 text-red-600" />
            Missing Skills ({results.missing_skills.length})
          </h2>
          <div className="space-y-3">
            {results.missing_skills.map((item, idx) => (
              <div key={idx} className="border-l-4 border-red-400 pl-4 py-2">
                <div className="flex items-center justify-between mb-1">
                  <p className="font-semibold text-gray-900">{item.skill}</p>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getImportanceColor(item.importance)}`}>
                    {item.importance}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{item.category}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Keyword Suggestions */}
      {results.keyword_suggestions?.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
            Keyword Suggestions ({results.keyword_suggestions.length})
          </h2>
          <div className="space-y-4">
            {results.keyword_suggestions.map((item, idx) => (
              <div key={idx} className="border-l-4 border-yellow-400 pl-4 py-2">
                <p className="font-semibold text-gray-900 mb-1">{item.keyword}</p>
                <p className="text-sm text-gray-600 mb-1"><strong>Context:</strong> {item.context}</p>
                <p className="text-sm text-gray-600"><strong>Why:</strong> {item.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resume Improvements */}
      {results.resume_improvements?.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-blue-600" />
            Resume Improvements
          </h2>
          <div className="space-y-6">
            {results.resume_improvements.map((section, idx) => (
              <div key={idx} className="border-l-4 border-blue-400 pl-4 py-2">
                <h3 className="font-bold text-lg text-gray-900 mb-2">{section.section}</h3>

                {section.current_content && section.current_content !== 'Missing' && (
                  <div className="mb-3">
                    <p className="text-sm font-semibold text-gray-700 mb-1">Current:</p>
                    <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">{section.current_content}</p>
                  </div>
                )}

                <div className="mb-3">
                  <p className="text-sm font-semibold text-green-700 mb-1">Suggested:</p>
                  <p className="text-sm text-gray-700 bg-green-50 p-2 rounded">{section.suggested_content}</p>
                </div>

                {section.improvements?.length > 0 && (
                  <div>
                    <p className="text-sm font-semibold text-blue-700 mb-1">Key Improvements:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {section.improvements.map((improvement, i) => (
                        <li key={i} className="text-sm text-gray-700">{improvement}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
