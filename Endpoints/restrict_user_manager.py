from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from get_db import get_db
from sql_app.models import UsersManagers
from Endpoints.authorization import verify_token


def restrict_user_manager(user_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    manager_id = int(current_user["manager_id"])  # Get the manager's ID

    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id).first():
        return user_id
    else:
        raise HTTPException(status_code=401, detail="You are not a manager of this client")




