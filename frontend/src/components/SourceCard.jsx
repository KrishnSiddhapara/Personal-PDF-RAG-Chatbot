import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = (e) => {
    e.stopPropagation();
    if (source.snippet) {
      navigator.clipboard.writeText(source.snippet);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="source-card" onClick={() => setExpanded(!expanded)}>
      <div className="source-card-header">
        <FileText size={13} style={{ color: 'var(--primary)', flexShrink: 0 }} />
        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '180px' }} title={source.filename}>
          {source.filename}
        </span>
        {source.page && <span className="source-page-tag">• Page {source.page}</span>}
        {source.snippet && (
          <span style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center' }}>
            {expanded ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </span>
        )}
      </div>

      {expanded && source.snippet && (
        <div className="source-snippet">
          <div>"{source.snippet}"</div>
          <button
            className="btn-text-action"
            style={{ fontSize: '0.7rem', marginTop: '6px' }}
            onClick={handleCopy}
          >
            {copied ? <Check size={12} /> : <Copy size={12} />}
            <span>{copied ? 'Copied' : 'Copy Text'}</span>
          </button>
        </div>
      )}
    </div>
  );
}
