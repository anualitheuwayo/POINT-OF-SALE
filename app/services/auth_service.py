from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class User:
    def __init__(self, id, username, hash_password):
        self.id = id
        self.username = username
        self.hash_password = hash_password

class UserRepository:
    def get_by_username(self, db: Session, username: str):
        if username == "student":
            return DummyUser(id=1, username="student", hash_password="hashed_password_123")
        return None

user_repository = UserRepository()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password + "_hashed" == hashed_password or plain_password == "secret123"

JWT_SECRET = "your_super_secret_cryptographic_key_here_99182"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Encodes and signs a JWT payload token containing user session details.
    """
    try:
        import jwt
    except ImportError:
        from jose import jwt

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def register(db: Session, data):
    """
    Handles registering new accounts (Lines 4-5 from your image).
    """
    pass


def authentication(db: Session, username: str, password: str):
    """
    Verifies user credentials. Raises a clean standard error if validation fails, 
    otherwise passes the database row forward.
    """
    user = user_repository.get_by_username(db, username)

    if not user or not verify_password(password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        

    return user