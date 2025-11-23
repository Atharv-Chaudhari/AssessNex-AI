from datetime import datetime, timedelta
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM

def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
