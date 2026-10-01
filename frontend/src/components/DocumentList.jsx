import React from 'react';
import { FileText, CheckCircle2, Loader2, XCircle, Trash2, CheckSquare, Square } from 'lucide-react';

function formatFileSize(bytes) {
  if (!bytes) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

export default function DocumentList({
  documents,
  selectedDocIds,
  onToggleSelect,
  onToggleSelectAll,
  onDelete
}) {
  const processedDocs = documents.filter(d => d.status === 'processed');
  const allSelected =
    processedDocs.length > 0 &&
    processedDocs.every(d => selectedDocIds.includes(d.document_id));

  return (
    <div className="doc-section">
      <div className="doc-section-header">
        <span className="doc-section-title">
          Your Documents ({documents.length})
        </span>
        {processedDocs.length > 0 && (
          <button
            className="btn-text-action"
            onClick={onToggleSelectAll}
            title={allSelected ? "Deselect All Documents" : "Select All Documents"}
          >
            {allSelected ? <CheckSquare size={14} /> : <Square size={14} />}
            <span>{allSelected ? 'Deselect All' : 'Select All'}</span>
          </button>
        )}
      </div>

      {documents.length === 0 ? (
        <div style={{
          fontSize: '0.8rem',
          color: 'var(--text-muted)',
          textAlign: 'center',
          padding: '24px 12px',
          border: '1px dashed var(--border)',
          borderRadius: 'var(--radius-md)'
        }}>
          No documents uploaded yet.
        </div>
      ) : (
        <div className="doc-list">
          {documents.map((doc) => {
            const isProcessed = doc.status === 'processed';
            const isProcessing = doc.status === 'processing' || doc.status === 'uploaded';
            const isFailed = doc.status === 'failed';
            const isSelected = selectedDocIds.includes(doc.document_id);

            return (
              <div
                key={doc.document_id}
                className={`doc-card ${isSelected ? 'selected' : ''}`}
                style={{ cursor: isProcessed ? 'pointer' : 'default' }}
                onClick={() => isProcessed && onToggleSelect(doc.document_id)}
              >
                <div className="doc-info">
                  <FileText className="doc-icon" size={18} />
                  
                  <div className="doc-details">
                    <span className="doc-name" title={doc.filename}>
                      {doc.filename}
                    </span>
                    <div className="doc-meta">
                      {isProcessed && (
                        <span className="badge processed">
                          <CheckCircle2 size={10} /> Ready
                        </span>
                      )}
                      {isProcessing && (
                        <span className="badge processing">
                          <Loader2 size={10} className="spin" /> Processing
                        </span>
                      )}
                      {isFailed && (
                        <span className="badge failed" title={doc.error_message || "Processing failed"}>
                          <XCircle size={10} /> Failed
                        </span>
                      )}
                      
                      {isProcessed && (
                        <>
                          <span>• {doc.page_count} pgs</span>
                          {doc.file_size > 0 && <span>• {formatFileSize(doc.file_size)}</span>}
                        </>
                      )}
                    </div>
                  </div>
                </div>

                <button
                  className="btn-icon"
                  title="Delete document and vectors"
                  aria-label={`Delete document ${doc.filename}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(doc.document_id);
                  }}
                >
                  <Trash2 size={15} />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
