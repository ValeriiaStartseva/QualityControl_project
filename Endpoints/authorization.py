from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Endpoints.hashing import pwd_context
from sql_app.base_model import BaseModelORM
from get_db import get_db
from sqlalchemy.orm import Session
from sql_app.models import Users
from jose import jwt, JWTError

login_router = APIRouter(prefix="/auth")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0/auth/login/")


class UserAuth(BaseModelORM):
    username: str
    password: str


def generate_token(user: Users):
    payload = {
        "sub": user.Email,
        "role_level": user.role.Level,
        "manager_id": user.Id,
        "role": "manager" if user.role.Level < 2 else 'customer',
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@login_router.get("/protected/")
def protected_route(current_user: dict = Depends(verify_token)):
    return {"message": "This route is protected!", "user": current_user}


@login_router.post("/login/")
def login_user(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.Email == user_auth.username).first()
    hash_p = user.Password
    db.close()

    if not user or not pwd_context.verify(user_auth.password, hash_p):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

