import React from 'react';
import { Sparkles } from 'lucide-react';

export default function LoadingIndicator() {
  return (
    <div className="chat-message assistant">
      <div className="avatar assistant">
        <Sparkles size={16} />
      </div>
      <div className="message-content-wrapper">
        <div className="message-bubble" style={{ padding: '12px 16px' }}>
          <div className="loading-indicator">
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
            <span>Retrieving context & generating response...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
