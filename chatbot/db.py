from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
import enum
import os
import bcrypt

from urllib.parse import quote_plus

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD"))  # encode special characters
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Debug: Print DB connection string (optional)
print(f"Connecting to DB at: {DB_HOST}:{DB_PORT}, DB name: {DB_NAME}")

# Create the engine and session
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum for user or assistant messages
class RoleEnum(enum.Enum):
    user = "user"
    assistant = "assistant"

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    sessions = relationship("ChatSession", back_populates="user")

# Session model
class ChatSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

# Message model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(Enum(RoleEnum))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")

# Function to create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency for FastAPI (optional)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
