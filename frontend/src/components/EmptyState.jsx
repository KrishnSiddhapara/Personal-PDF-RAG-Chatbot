import React from 'react';
import { FileSearch, Sparkles } from 'lucide-react';

export default function EmptyState({ onSelectPrompt, totalDocCount }) {
  const suggestedPrompts = [
    "What is this document about?",
    "Summarize the main points of the document.",
    "What are the key conclusions or recommendations?",
    "Explain the primary concepts discussed."
  ];

  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <FileSearch size={28} />
      </div>

      <h2 className="empty-state-title">Personal PDF Assistant</h2>
      
      <p className="empty-state-text">
        {totalDocCount > 0
          ? "Ask questions about your uploaded documents. The AI will retrieve grounded answers with exact source citations."
          : "Upload one or more PDF files in the sidebar to start chatting with your documents."}
      </p>

      {totalDocCount > 0 && (
        <div className="suggested-prompts">
          <div className="suggested-prompts-label">Try asking:</div>
          {suggestedPrompts.map((promptText, index) => (
            <button
              key={index}
              className="prompt-pill"
              onClick={() => onSelectPrompt(promptText)}
            >
              <span>"{promptText}"</span>
              <Sparkles size={14} style={{ color: 'var(--primary)', opacity: 0.8 }} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
