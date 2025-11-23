"""PostgreSQL-based storage for conversations using Neon."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncpg
from .config import DATABASE_URL

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """Get or create the database connection pool."""
    global _pool
    if _pool is None:
        # Convert postgresql:// to postgresql+asyncpg:// format if needed
        # asyncpg uses postgresql:// directly
        _pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        # Initialize tables
        await init_db(_pool)
    return _pool


async def init_db(pool: asyncpg.Pool):
    """Initialize database tables."""
    async with pool.acquire() as conn:
        # Create conversations table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id VARCHAR(255) PRIMARY KEY,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                title VARCHAR(500) NOT NULL DEFAULT 'New Conversation',
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create messages table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                role VARCHAR(50) NOT NULL,
                content TEXT,
                stage1 JSONB,
                stage2 JSONB,
                stage3 JSONB,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                message_order INTEGER NOT NULL
            )
        """)
        
        # Create indexes
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
            ON messages(conversation_id)
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_order 
            ON messages(conversation_id, message_order)
        """)


async def create_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Create a new conversation.

    Args:
        conversation_id: Unique identifier for the conversation

    Returns:
        New conversation dict
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO conversations (id, created_at, title)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
        """, conversation_id, datetime.utcnow(), "New Conversation")
    
    return {
        "id": conversation_id,
        "created_at": datetime.utcnow().isoformat(),
        "title": "New Conversation",
        "messages": []
    }


async def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Load a conversation from storage.

    Args:
        conversation_id: Unique identifier for the conversation

    Returns:
        Conversation dict or None if not found
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Get conversation metadata
        row = await conn.fetchrow("""
            SELECT id, created_at, title
            FROM conversations
            WHERE id = $1
        """, conversation_id)
        
        if row is None:
            return None
        
        # Get messages
        message_rows = await conn.fetch("""
            SELECT role, content, stage1, stage2, stage3
            FROM messages
            WHERE conversation_id = $1
            ORDER BY message_order ASC
        """, conversation_id)
        
        messages = []
        for msg_row in message_rows:
            if msg_row['role'] == 'user':
                messages.append({
                    "role": "user",
                    "content": msg_row['content']
                })
            else:
                messages.append({
                    "role": "assistant",
                    "stage1": json.loads(msg_row['stage1']) if msg_row['stage1'] else None,
                    "stage2": json.loads(msg_row['stage2']) if msg_row['stage2'] else None,
                    "stage3": json.loads(msg_row['stage3']) if msg_row['stage3'] else None
                })
        
        return {
            "id": row['id'],
            "created_at": row['created_at'].isoformat(),
            "title": row['title'],
            "messages": messages
        }


async def save_conversation(conversation: Dict[str, Any]):
    """
    Save a conversation to storage.
    Note: This is kept for compatibility but messages are saved individually.

    Args:
        conversation: Conversation dict to save
    """
    # Messages are saved individually via add_user_message/add_assistant_message
    # Just update the title if needed
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE conversations
            SET title = $1, updated_at = $2
            WHERE id = $3
        """, conversation.get('title', 'New Conversation'), datetime.utcnow(), conversation['id'])


async def list_conversations() -> List[Dict[str, Any]]:
    """
    List all conversations (metadata only).

    Returns:
        List of conversation metadata dicts
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                c.id,
                c.created_at,
                c.title,
                COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id, c.created_at, c.title
            ORDER BY c.created_at DESC
        """)
        
        return [
            {
                "id": row['id'],
                "created_at": row['created_at'].isoformat(),
                "title": row['title'],
                "message_count": row['message_count']
            }
            for row in rows
        ]


async def add_user_message(conversation_id: str, content: str):
    """
    Add a user message to a conversation.

    Args:
        conversation_id: Conversation identifier
        content: User message content
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Get current message count to set order
        count = await conn.fetchval("""
            SELECT COUNT(*) FROM messages WHERE conversation_id = $1
        """, conversation_id)
        
        await conn.execute("""
            INSERT INTO messages (conversation_id, role, content, message_order)
            VALUES ($1, $2, $3, $4)
        """, conversation_id, "user", content, count)


async def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict[str, Any]],
    stage2: List[Dict[str, Any]],
    stage3: Dict[str, Any]
):
    """
    Add an assistant message with all 3 stages to a conversation.

    Args:
        conversation_id: Conversation identifier
        stage1: List of individual model responses
        stage2: List of model rankings
        stage3: Final synthesized response
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Get current message count to set order
        count = await conn.fetchval("""
            SELECT COUNT(*) FROM messages WHERE conversation_id = $1
        """, conversation_id)
        
        await conn.execute("""
            INSERT INTO messages (conversation_id, role, stage1, stage2, stage3, message_order)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, 
            conversation_id,
            "assistant",
            json.dumps(stage1),
            json.dumps(stage2),
            json.dumps(stage3),
            count
        )


async def update_conversation_title(conversation_id: str, title: str):
    """
    Update the title of a conversation.

    Args:
        conversation_id: Conversation identifier
        title: New title for the conversation
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE conversations
            SET title = $1, updated_at = $2
            WHERE id = $3
        """, title, datetime.utcnow(), conversation_id)
