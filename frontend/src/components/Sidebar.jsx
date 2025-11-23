import { Plus, MessageSquare, X } from 'lucide-react';
import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  isOpen,
  onClose,
}) {
  return (
    <>
      <div className={`sidebar-overlay ${isOpen ? 'open' : ''}`} onClick={onClose} />
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="header-top">
            <h1>LLM Council</h1>
            <button className="close-sidebar-btn" onClick={onClose}>
              <X size={24} />
            </button>
          </div>
          <button className="new-conversation-btn" onClick={onNewConversation}>
            <Plus size={18} />
            <span>New Conversation</span>
          </button>
        </div>

        <div className="conversation-list">
          {conversations.length === 0 ? (
            <div className="no-conversations">
              <MessageSquare size={48} opacity={0.2} />
              <p>No conversations yet</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${conv.id === currentConversationId ? 'active' : ''
                  }`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <MessageSquare size={18} className="conv-icon" />
                <div className="conversation-info">
                  <div className="conversation-title">
                    {conv.title || 'New Conversation'}
                  </div>
                  <div className="conversation-meta">
                    {conv.message_count} messages
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
