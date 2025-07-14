from chatbot.db import SessionLocal, ChatSession, Message, RoleEnum

def create_session(user_id: int, title: str):
    db = SessionLocal()
    session = ChatSession(title=title, user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()
    return {"session_id": session.id}

def get_user_sessions(user_id: int):
    db = SessionLocal()
    sessions = db.query(ChatSession).filter_by(user_id=user_id).all()
    db.close()
    return [{"id": s.id, "title": s.title} for s in sessions]

def get_session_history(session_id: int):
    db = SessionLocal()
    messages = db.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all()
    db.close()
    return [{"role": m.role.value, "content": m.content} for m in messages]

def append_to_session(session_id: int, role: str, content: str):
    db = SessionLocal()
    message = Message(session_id=session_id, role=RoleEnum(role), content=content)
    db.add(message)
    db.commit()
    db.close()