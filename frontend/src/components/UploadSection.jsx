import { Upload, FileText } from 'lucide-react';

export default function UploadSection({ onFileChange, onJobDescriptionChange, fileName, jobDescription }) {
  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Upload className="w-5 h-5" />
          Upload Resume
        </h2>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            Resume File (PDF or DOCX)
          </label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={onFileChange}
            className="input-file"
          />
          {fileName && (
            <p className="text-sm text-gray-600 flex items-center gap-2 mt-2">
              <FileText className="w-4 h-4" />
              {fileName}
            </p>
          )}
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <FileText className="w-5 h-5" />
          Job Description
        </h2>
        <textarea
          value={jobDescription}
          onChange={onJobDescriptionChange}
          placeholder="Paste the job description here..."
          rows={12}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
        />
        <p className="text-sm text-gray-500 mt-2">
          Paste the complete job description including requirements, responsibilities, and qualifications.
        </p>
      </div>
    </div>
  );
}
