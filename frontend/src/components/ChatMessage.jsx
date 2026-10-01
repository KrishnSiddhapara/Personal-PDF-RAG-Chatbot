import React, { useState } from 'react';
import SourceCard from './SourceCard';
import { User, Sparkles, Copy, Check, Info } from 'lucide-react';

function CodeBlock({ codeText, language }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(codeText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span>{language || 'code'}</span>
        <button
          onClick={handleCopy}
          style={{
            background: 'none',
            border: 'none',
            color: '#94a3b8',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontSize: '0.75rem'
          }}
        >
          {copied ? <Check size={12} /> : <Copy size={12} />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
      </div>
      <div className="code-block-body">
        <code>{codeText}</code>
      </div>
    </div>
  );
}

function renderMarkdownText(text) {
  if (!text) return null;

  const paragraphs = text.split(/\n\n+/);

  return paragraphs.map((para, idx) => {
    // Check if code block
    if (para.startsWith('```') && para.endsWith('```')) {
      const firstLineEnd = para.indexOf('\n');
      let lang = 'code';
      let codeContent = para.slice(3, -3);
      if (firstLineEnd !== -1) {
        lang = para.slice(3, firstLineEnd).trim() || 'code';
        codeContent = para.slice(firstLineEnd + 1, -3);
      }
      return <CodeBlock key={idx} codeText={codeContent.trim()} language={lang} />;
    }

    // Check if bullet or numbered list
    const lines = para.split('\n');
    const isBulletList = lines.every(line => line.trim().startsWith('- ') || line.trim().startsWith('* ') || /^\d+\.\s/.test(line.trim()));

    if (isBulletList) {
      return (
        <ul key={idx} style={{ margin: '8px 0 8px 20px' }}>
          {lines.map((line, lIdx) => {
            const cleanLine = line.trim().replace(/^[-*]\s+|\d+\.\s+/, '');
            return <li key={lIdx}>{formatInlineMarkdown(cleanLine)}</li>;
          })}
        </ul>
      );
    }

    return (
      <p key={idx}>
        {lines.map((line, lIdx) => (
          <React.Fragment key={lIdx}>
            {formatInlineMarkdown(line)}
            {lIdx < lines.length - 1 && <br />}
          </React.Fragment>
        ))}
      </p>
    );
  });
}

function formatInlineMarkdown(text) {
  const parts = text.split(/(\*\*.*?\*\*|`.*?`)/g);

  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i}>{part.slice(1, -1)}</code>;
    }
    return part;
  });
}

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  const isNoContext = !isUser && message.text.includes("couldn't find enough information");

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className={`avatar ${isUser ? 'user' : 'assistant'}`}>
        {isUser ? <User size={16} /> : <Sparkles size={16} />}
      </div>
      
      <div className="message-content-wrapper">
        <div className="message-bubble">
          {isNoContext ? (
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px',
              backgroundColor: 'var(--surface-secondary)',
              padding: '12px 14px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border)'
            }}>
              <Info size={18} style={{ color: 'var(--text-secondary)', flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>Not found in documents</strong>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '2px', marginBottom: 0 }}>
                  {message.text}
                </p>
              </div>
            </div>
          ) : (
            <div className="markdown-body">
              {renderMarkdownText(message.text)}
            </div>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="sources-section">
            <div className="sources-label">
              <span>Retrieved Sources ({message.sources.length})</span>
            </div>
            <div className="sources-grid">
              {message.sources.map((src, i) => (
                <SourceCard key={i} source={src} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
