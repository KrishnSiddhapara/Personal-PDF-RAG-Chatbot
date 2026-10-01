import React, { useRef, useState } from 'react';
import { UploadCloud, Loader2 } from 'lucide-react';

export default function PDFUploader({ onUpload, isUploading }) {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onUpload(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(Array.from(e.target.files));
      e.target.value = '';
    }
  };

  return (
    <div
      className={`uploader-card ${dragActive ? 'drag-active' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => !isUploading && fileInputRef.current && fileInputRef.current.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,application/pdf"
        className="file-input"
        onChange={handleChange}
        disabled={isUploading}
      />
      
      {isUploading ? (
        <Loader2 className="uploader-icon spin" />
      ) : (
        <UploadCloud className="uploader-icon" />
      )}

      <div className="uploader-title">
        {isUploading ? 'Processing Document...' : 'Drop your PDF here'}
      </div>
      <div className="uploader-subtext">
        {isUploading
          ? 'Extracting text & creating vectors...'
          : 'or click to Browse Files (up to 25 MB)'}
      </div>
    </div>
  );
}
