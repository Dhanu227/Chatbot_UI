from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from chatbot.db import SessionLocal, init_db, User, ChatSession, Message, RoleEnum
from chatbot.llm import generate_response
import bcrypt
import uuid
from pydantic import BaseModel
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_login_page():
    return FileResponse(os.path.join(static_dir, "login.html"))

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize DB on app start
init_db()
print("✅ Database initialized.")

# ----------- Schemas -----------
class UserCredentials(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    user_id: int
    session_id: int
    message: str

class NewSessionRequest(BaseModel):
    user_id: int

# ----------- Auth Endpoints -----------
@app.post("/register")
def register_user(data: UserCredentials, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        return JSONResponse(status_code=400, content={"message": "Username already taken"})

    hashed_pwd = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    user = User(username=data.username, password=hashed_pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user_id": user.id}

@app.post("/login")
def login_user(data: UserCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})

    return {"message": "Login successful", "user_id": user.id}

# ----------- Session Management -----------
@app.post("/new_session")
def create_session(req: NewSessionRequest, db: Session = Depends(get_db)):
    session = ChatSession(user_id=req.user_id, title=f"Session_{uuid.uuid4().hex[:5]}")
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "title": session.title}

@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc()).all()
    return [{"id": s.id, "title": s.title} for s in sessions]

# ----------- Chat Endpoint (uses generate_response) -----------
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # Save user message
    user_msg = Message(session_id=req.session_id, role=RoleEnum.user, content=req.message)
    db.add(user_msg)

    try:
        # Collect full session message history
        messages = db.query(Message).filter(Message.session_id == req.session_id).order_by(Message.timestamp).all()
        chat_history = [{"role": m.role.value, "content": m.content} for m in messages]
        chat_history.append({"role": "user", "content": req.message})

        # Generate assistant response
        assistant_reply = generate_response(chat_history)

    except Exception as e:
        print("❌ Error generating response:", e)
        assistant_reply = f"[Error] Failed to generate reply: {e}"

    # Save assistant reply
    assistant_msg = Message(session_id=req.session_id, role=RoleEnum.assistant, content=assistant_reply)
    db.add(assistant_msg)
    db.commit()

    return {"reply": assistant_reply}

# ----------- Get Message History -----------
@app.get("/session-messages/{user_id}/{session_id}")
def get_messages(user_id: int, session_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).join(ChatSession).filter(
        ChatSession.user_id == user_id,
        Message.session_id == session_id
    ).order_by(Message.timestamp).all()

    return [{"role": m.role.value, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in messages]
