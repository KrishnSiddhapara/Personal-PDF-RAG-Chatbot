import React from 'react';
import { FileText, Menu, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';

export default function Header({ health, onToggleMobileSidebar }) {
  const isOnline = health && health.status === 'ok';
  const hasKey = health && health.has_api_key;

  return (
    <header className="app-header">
      <div className="header-left">
        <button
          className="btn-mobile-menu"
          onClick={onToggleMobileSidebar}
          title="Toggle Mobile Sidebar"
        >
          <Menu size={20} />
        </button>

        <div className="brand">
          <div className="brand-icon">
            <FileText size={18} />
          </div>
          <div className="brand-titles">
            <h1 className="brand-title">Personal PDF Assistant</h1>
            <span className="brand-subtitle">Chat with your documents using AI</span>
          </div>
        </div>
      </div>

      <div className="header-right">
        {isOnline ? (
          hasKey ? (
            <div className="status-pill ready">
              <CheckCircle2 size={13} />
              <span>Gemini Ready</span>
            </div>
          ) : (
            <div className="status-pill warning">
              <AlertTriangle size={13} />
              <span>API Key Missing</span>
            </div>
          )
        ) : (
          <div className="status-pill error">
            <XCircle size={13} />
            <span>Backend Offline</span>
          </div>
        )}
      </div>
    </header>
  );
}
