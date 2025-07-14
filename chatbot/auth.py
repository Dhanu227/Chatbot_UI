from chatbot.db import SessionLocal, User
import bcrypt

def register_user(username: str, password: str):
    db = SessionLocal()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.close()
    return {"msg": "Registered"}

def login_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    db.close()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return {"user_id": user.id, "username": user.username}
    return {"error": "Invalid credentials"}