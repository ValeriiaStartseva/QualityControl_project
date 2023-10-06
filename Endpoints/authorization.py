from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from Endpoints.hashing import pwd_context
from sql_app.base_model import BaseModelORM
from get_db import get_db
from sqlalchemy.orm import Session
from sql_app.models import Users
from jose import jwt

login_router = APIRouter(prefix="/api/v0")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class UserAuth(BaseModelORM):
    Email: str
    Password: str


def generate_token(user: Users):
    if user.RoleId < 2:
        payload = {
            "sub": user.Email,
            "role": "manager",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
    else:
        payload = {
            "sub": user.Email,
            "role": "customer",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# def decode_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#
#
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid credentials")


# Create a route for user login and token generation
@login_router.post("/login/")
def login_user(user_auth: UserAuth, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.Email == user_auth.Email).first()
    hash_p = user.Password
    db.close()

    if not user or not pwd_context.verify(user_auth.Password, hash_p):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

