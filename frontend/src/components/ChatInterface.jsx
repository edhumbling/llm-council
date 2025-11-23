import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Menu, Loader2 } from 'lucide-react';
import Stage1 from './Stage1';
import Stage2 from './Stage2';
import Stage3 from './Stage3';
import './ChatInterface.css';

export default function ChatInterface({
  conversation,
  onSendMessage,
  isLoading,
  onOpenSidebar,
}) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!conversation) {
    return (
      <div className="chat-interface">
        <div className="chat-header">
          <button className="menu-btn" onClick={onOpenSidebar}>
            <Menu size={24} />
          </button>
          <span className="header-title">LLM Council</span>
        </div>
        <div className="messages-container">
          <div className="empty-state">
            <h2>LLM Council</h2>
            <p>Get insights from multiple AI models working together</p>
            <div className="example-prompts">
              <div className="example-prompt" onClick={() => {
                const input = document.querySelector('.message-input');
                if (input) input.value = "Explain quantum computing in simple terms";
              }}>
                <h3>🔬 Science</h3>
                <p>Explain quantum computing in simple terms</p>
              </div>
              <div className="example-prompt" onClick={() => {
                const input = document.querySelector('.message-input');
                if (input) input.value = "Write a haiku about artificial intelligence";
              }}>
                <h3>✨ Creative</h3>
                <p>Write a haiku about artificial intelligence</p>
              </div>
              <div className="example-prompt" onClick={() => {
                const input = document.querySelector('.message-input');
                if (input) input.value = "What are the best practices for API design?";
              }}>
                <h3>💻 Code</h3>
                <p>What are the best practices for API design?</p>
              </div>
              <div className="example-prompt" onClick={() => {
                const input = document.querySelector('.message-input');
                if (input) input.value = "How do I start learning machine learning?";
              }}>
                <h3>📚 Learning</h3>
                <p>How do I start learning machine learning?</p>
              </div>
            </div>
          </div>
        </div>
        <form className="input-form" onSubmit={(e) => { e.preventDefault(); }}>
          <textarea
            className="message-input"
            placeholder="Ask anything..."
            disabled
            rows={1}
          />
          <button type="submit" className="send-button" disabled>
            <Send size={20} />
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <button className="menu-btn" onClick={onOpenSidebar}>
          <Menu size={24} />
        </button>
        <span className="header-title">{conversation.title || 'New Conversation'}</span>
      </div>

      <div className="messages-container">
        {conversation.messages.length === 0 ? (
          <div className="empty-state">
            <h2>Start a conversation</h2>
            <p>Ask a question to consult the LLM Council</p>
          </div>
        ) : (
          conversation.messages.map((msg, index) => (
            <div key={index} className="message-group">
              {msg.role === 'user' ? (
                <div className="user-message">
                  <div className="message-label">You</div>
                  <div className="message-content">
                    <div className="markdown-content">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="assistant-message">
                  <div className="message-label">LLM Council</div>

                  {/* Stage 1 */}
                  {msg.loading?.stage1 && (
                    <div className="stage-loading">
                      <Loader2 className="spinner-icon" size={16} />
                      <span>Running Stage 1: Collecting individual responses...</span>
                    </div>
                  )}
                  {msg.stage1 && <Stage1 responses={msg.stage1} />}

                  {/* Stage 2 */}
                  {msg.loading?.stage2 && (
                    <div className="stage-loading">
                      <Loader2 className="spinner-icon" size={16} />
                      <span>Running Stage 2: Peer rankings...</span>
                    </div>
                  )}
                  {msg.stage2 && (
                    <Stage2
                      rankings={msg.stage2}
                      labelToModel={msg.metadata?.label_to_model}
                      aggregateRankings={msg.metadata?.aggregate_rankings}
                    />
                  )}

                  {/* Stage 3 */}
                  {msg.loading?.stage3 && (
                    <div className="stage-loading">
                      <Loader2 className="spinner-icon" size={16} />
                      <span>Running Stage 3: Final synthesis...</span>
                    </div>
                  )}
                  {msg.stage3 && <Stage3 finalResponse={msg.stage3} />}
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="loading-indicator">
            <Loader2 className="spinner-icon" size={20} />
            <span>Consulting the council...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <textarea
          className="message-input"
          placeholder={conversation.messages.length === 0
            ? "Ask your question..."
            : "Continue the conversation..."}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? <Loader2 className="spinner-icon" size={20} /> : <Send size={20} />}
        </button>
      </form>
    </div>
  );
}
