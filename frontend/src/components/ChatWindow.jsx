import React, { useRef, useEffect, useState } from 'react';
import ChatMessage from './ChatMessage';
import LoadingIndicator from './LoadingIndicator';
import EmptyState from './EmptyState';
import { Send, RotateCcw, Search } from 'lucide-react';

export default function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  onClearChat,
  selectedDocCount,
  totalDocCount
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleSelectPrompt = (promptText) => {
    onSendMessage(promptText);
  };

  const isFilterActive = selectedDocCount > 0 && selectedDocCount < totalDocCount;

  return (
    <div className="chat-panel">
      <div className="messages-container">
        {messages.length === 0 ? (
          <EmptyState
            onSelectPrompt={handleSelectPrompt}
            totalDocCount={totalDocCount}
          />
        ) : (
          <div className="messages-inner">
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} />
            ))}
            {isLoading && <LoadingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <div className="chat-input-inner">
          <div className="filter-indicator">
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Search size={12} />
              {isFilterActive
                ? `Searching ${selectedDocCount} selected document(s)`
                : totalDocCount > 0
                ? `Searching across all ${totalDocCount} document(s)`
                : 'Upload a PDF to start asking questions'}
            </span>

            {messages.length > 0 && (
              <button
                className="btn-text-action"
                onClick={onClearChat}
                style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}
              >
                <RotateCcw size={12} />
                <span>Clear Conversation</span>
              </button>
            )}
          </div>

          <div className="input-container">
            <textarea
              rows="1"
              className="chat-textarea"
              placeholder={
                totalDocCount === 0
                  ? "Upload a PDF document first..."
                  : "Ask a question about your documents... (Shift+Enter for new line)"
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading || totalDocCount === 0}
            />

            <button
              className="btn-send"
              onClick={handleSubmit}
              disabled={!input.trim() || isLoading || totalDocCount === 0}
              title="Send message (Enter)"
              aria-label="Send message"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
