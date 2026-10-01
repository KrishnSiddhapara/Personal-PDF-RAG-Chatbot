import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import PDFUploader from './components/PDFUploader';
import DocumentList from './components/DocumentList';
import ChatWindow from './components/ChatWindow';
import {
  checkHealth,
  getDocuments,
  uploadDocuments,
  deleteDocument,
  sendChatMessage
} from './services/api';

export default function App() {
  const [health, setHealth] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [selectedDocIds, setSelectedDocIds] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [errorToast, setErrorToast] = useState(null);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const showError = (msg) => {
    setErrorToast(msg);
    setTimeout(() => setErrorToast(null), 5000);
  };

  const loadData = async () => {
    try {
      const hData = await checkHealth();
      setHealth(hData);
      
      const docList = await getDocuments();
      setDocuments(docList);

      const processedIds = docList
        .filter(d => d.status === 'processed')
        .map(d => d.document_id);

      setSelectedDocIds(prev => {
        if (prev.length === 0) {
          return processedIds;
        }
        return prev.filter(id => processedIds.includes(id));
      });
    } catch (err) {
      console.error('Failed loading initial data:', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async (files) => {
    if (!files || files.length === 0) return;
    setIsUploading(true);
    try {
      const res = await uploadDocuments(files);
      if (res.documents) {
        setDocuments(res.documents);
        const newDocIds = res.documents
          .filter(d => d.status === 'processed')
          .map(d => d.document_id);
        setSelectedDocIds(prev => Array.from(new Set([...prev, ...newDocIds])));
      }
    } catch (err) {
      showError(err.message || 'Failed to upload document(s).');
    } finally {
      setIsUploading(false);
      loadData();
    }
  };

  const handleDelete = async (docId) => {
    try {
      await deleteDocument(docId);
      setDocuments(prev => prev.filter(d => d.document_id !== docId));
      setSelectedDocIds(prev => prev.filter(id => id !== docId));
    } catch (err) {
      showError(err.message || 'Failed to delete document.');
    }
  };

  const handleToggleSelect = (docId) => {
    setSelectedDocIds(prev =>
      prev.includes(docId) ? prev.filter(id => id !== docId) : [...prev, docId]
    );
  };

  const handleToggleSelectAll = () => {
    const processedIds = documents
      .filter(d => d.status === 'processed')
      .map(d => d.document_id);

    const isAllSelected =
      processedIds.length > 0 &&
      processedIds.every(id => selectedDocIds.includes(id));

    if (isAllSelected) {
      setSelectedDocIds([]);
    } else {
      setSelectedDocIds(processedIds);
    }
  };

  const handleSendMessage = async (questionText) => {
    const userMsg = { role: 'user', text: questionText };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await sendChatMessage(
        questionText,
        selectedDocIds.length > 0 ? selectedDocIds : [],
        conversationId
      );

      if (res.conversation_id) {
        setConversationId(res.conversation_id);
      }

      const assistantMsg = {
        role: 'assistant',
        text: res.answer,
        sources: res.sources || []
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      showError(err.message || 'Failed to get answer from chatbot.');
      const errorMsg = {
        role: 'assistant',
        text: '⚠️ An error occurred while retrieving or processing your question. Please check backend status or API key.'
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="app-container">
      <Header
        health={health}
        onToggleMobileSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
      />

      {errorToast && (
        <div style={{
          position: 'fixed',
          top: '70px',
          right: '20px',
          background: 'var(--error)',
          color: 'white',
          padding: '10px 16px',
          borderRadius: 'var(--radius-sm)',
          zIndex: 1000,
          boxShadow: 'var(--shadow-md)',
          fontSize: '0.85rem'
        }}>
          {errorToast}
        </div>
      )}

      <div className="app-main">
        {/* Mobile backdrop overlay */}
        <div
          className={`mobile-overlay ${mobileSidebarOpen ? 'open' : ''}`}
          onClick={() => setMobileSidebarOpen(false)}
        />

        <aside className={`sidebar ${mobileSidebarOpen ? 'open' : ''}`}>
          <PDFUploader onUpload={handleUpload} isUploading={isUploading} />
          
          <DocumentList
            documents={documents}
            selectedDocIds={selectedDocIds}
            onToggleSelect={handleToggleSelect}
            onToggleSelectAll={handleToggleSelectAll}
            onDelete={handleDelete}
          />
        </aside>

        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100%' }}>
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            onClearChat={handleClearChat}
            selectedDocCount={selectedDocIds.length}
            totalDocCount={documents.filter(d => d.status === 'processed').length}
          />
        </main>
      </div>
    </div>
  );
}
