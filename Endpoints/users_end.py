from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status
from get_db import get_db
from sql_app.models import Roles, Users, UsersManagers, CollectUser
from Endpoints.authorization import verify_token
from sqlalchemy import update, and_
from Endpoints.restrict_user_manager import restrict_user_manager
import datetime

users_router = APIRouter(prefix="/auth")


# 2.1.
@users_router.get("/users/{manager_id}/subordinates")
async def get_subordinates(manager_id: int, db: Session = Depends(get_db)):
    subordinates = db.query(Users).\
        join(CollectUser, and_(Users.UserId == CollectUser.Id)).\
        join(Roles, and_(Users.RoleId == Roles.Id)).\
        join(UsersManagers, and_(Users.Id == UsersManagers.UserId)).\
        filter(UsersManagers.ManagerId == manager_id).all()

    subordinates_data = []
    for user in subordinates:
        subordinates_data.append({
            "Login": user.collect.Login,
            "Name": user.collect.FullName,
            "Role": user.role.Name,
            "EmploymentDate": user.EmploymentDate,
            "DismissalDate": user.DismissalDate,
            "Email": user.Email,
            "Probation": user.Probation,
        })

    return subordinates_data


# 2.2.
@users_router.get("/users/users_by_higher_level")
def get_users_with_higher_level(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    role_level_current_user = int(current_user.get("role_level"))
    query = db.query(Users).\
        join(CollectUser, and_(Users.UserId == CollectUser.Id)).\
        join(Roles).filter(Roles.Level > role_level_current_user).all()
    users = []
    for user in query:
        users.append({
            "Login": user.collect.Login,
            "Name": user.collect.FullName,
            "Role": user.role.Name,
            "EmploymentDate": user.EmploymentDate,
            "DismissalDate": user.DismissalDate,
        })
    return users


# 2.3.
@users_router.patch("/users/change_probation")
async def change_probation(user_id: int, new_probation: int, current_user: dict = Depends(verify_token),
                           db: Session = Depends(get_db)):
    if restrict_user_manager(user_id, current_user, db):
        query = update(Users).values(Probation=new_probation).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user are not an manager of a client!')
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.4
@users_router.patch("/users/change_head_of_user")
async def change_head(user_id: int, new_head: int, current_user: dict = Depends(verify_token),
                      db: Session = Depends(get_db)):
    role_level_current_user = int(current_user.get("role_level"))
    role_level = db.query(Roles).join(Users).filter(Users.Id == user_id).first()
    role_level_user = role_level.Level
    if db.query(UsersManagers).filter(restrict_user_manager).first() \
            or role_level_user < role_level_current_user:
        query = update(UsersManagers).values(ManagerId=new_head).where(UsersManagers.UserId == user_id)
        db.execute(query)
        db.commit()
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.5.
@users_router.patch("/users/quit")
def quit_user(user_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    current_date = datetime.date.today()
    if restrict_user_manager(user_id, current_user, db):
        query = update(Users).values(DismissalDate=current_date).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    return Response(status_code=status.HTTP_200_OK, description='User was successfully quited!')


# 2.6.
@users_router.patch("/users/change_role")
def change_role(user_id: int, new_role: int,  current_user: dict = Depends(verify_token),
                db: Session = Depends(get_db)):
    role_level_current_user = int(current_user.get("role_level"))
    role_level = db.query(Roles).join(Users).filter(Users.Id == user_id).first()
    role_level_user = role_level.Level
    if restrict_user_manager(user_id, current_user, db) or role_level_user < role_level_current_user:
        query = update(Users).values(RoleId=new_role).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.7.
@users_router.delete("/users/delete_from_subordinates")
def delete_from_subordinates(user_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    if restrict_user_manager(user_id, current_user, db):
        row_to_delete = db.query(UsersManagers).filter(UsersManagers.UserId == user_id).first()
        if row_to_delete:
            db.delete(row_to_delete)
            db.commit()
    return Response(status_code=status.HTTP_200_OK, description='Deleted!')
