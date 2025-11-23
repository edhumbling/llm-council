/**
 * API client for the LLM Council backend.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Generate or retrieve device ID
function getDeviceId() {
  let deviceId = localStorage.getItem('llm-council-device-id');
  if (!deviceId) {
    // Generate a unique device ID (UUID-like)
    deviceId = 'device_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('llm-council-device-id', deviceId);
  }
  return deviceId;
}

export const api = {
  /**
   * List all conversations for this device.
   */
  async listConversations() {
    try {
      const deviceId = getDeviceId();
      const response = await fetch(`${API_BASE}/api/conversations?device_id=${encodeURIComponent(deviceId)}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return response.json();
    } catch (error) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error(`Cannot connect to backend at ${API_BASE}. Is the server running?`);
      }
      throw error;
    }
  },

  /**
   * Create a new conversation for this device.
   */
  async createConversation() {
    const deviceId = getDeviceId();
    const response = await fetch(`${API_BASE}/api/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device_id: deviceId }),
    });
    return response.json();
  },

  /**
   * Get a specific conversation by ID.
   */
  async getConversation(id) {
    const response = await fetch(`${API_BASE}/api/conversations/${id}`);
    return response.json();
  },

  /**
   * Send a message and stream the response.
   */
  async sendMessageStream(conversationId, content, onEvent) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/message/stream`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') {
            onEvent('complete', {});
            return;
          }

          try {
            const event = JSON.parse(data);
            onEvent(event.type, event);
          } catch (e) {
            console.error('Failed to parse event:', e, data);
          }
        }
      }
    }
  },

  /**
   * Send a message (non-streaming version).
   */
  async sendMessage(conversationId, content) {
    const response = await fetch(
      `${API_BASE}/api/conversations/${conversationId}/message`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      }
    );
    return response.json();
  },
};
