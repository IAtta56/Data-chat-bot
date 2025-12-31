from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    files: List["File"] = Relationship(back_populates="owner")
    chats: List["ChatSession"] = Relationship(back_populates="user")

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    filepath: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="files")
    chat_sessions: List["ChatSession"] = Relationship(back_populates="file")

class ChatSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="New Chat")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    file_id: Optional[int] = Field(default=None, foreign_key="file.id")

    user: User = Relationship(back_populates="chats")
    file: Optional[File] = Relationship(back_populates="chat_sessions")
    messages: List["Message"] = Relationship(back_populates="session")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    role: str # "user" or "assistant"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: int = Field(foreign_key="chatsession.id")

    session: ChatSession = Relationship(back_populates="messages")
