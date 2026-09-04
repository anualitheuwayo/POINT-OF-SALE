from fastapi import Depends
from fastapi.security import QAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import get_user_from_token

qauth2_scheme =QAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(qauth2_scheme), db: Session = Depends(get_db)):
    user =  get_user_from_token(db, token)
    return user