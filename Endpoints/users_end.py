from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status
from get_db import get_db
from sql_app.schemas import UsersBase
from sql_app.models import Roles, Users, UsersManagers
from Endpoints.authorization import verify_token
from sqlalchemy import update, delete, and_
import datetime

users_router = APIRouter(prefix="/auth")


# 2.1. GET ендпоінт для отримання підлеглих (підлеглих по таблиці UsersManagers можна дивитися)
# (тут треба повертати логін, ім'я, роль, дату прийому на роботу, дату звільнення, e-mail та стан випробувального
# терміну (Probation))
@users_router.get("/users/{manager_id}/subordinates", response_model=list[UsersBase])
async def get_subordinates(manager_id: int, db: Session = Depends(get_db)):
    subordinates = db.query(Users).join(UsersManagers, and_(Users.Id == UsersManagers.UserId)).\
        filter(UsersManagers.ManagerId == manager_id)
    return [UsersBase.model_validate(model) for model in subordinates]


# 2.2. GET ендпоінт для отримання списку всіх користувачів, в яких level ролі > за level ролі користувача, що відправляє
# запит (тут треба повертати логін, ім'я, роль, дату прийому на роботу та дату звільнення)
@users_router.get("/users/users_by_higher_level", response_model=list[UsersBase])
def get_users_with_higher_level(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    role_level_current_user = int(current_user.get("role_level"))
    query = db.query(Users).join(Roles).filter(Roles.Level > role_level_current_user).all()
    return [UsersBase.model_validate(model) for model in query]


# 2.3. PATCH ендпоінт для зміни статусу випробувального терміну (поле Probation), може змінювати тільки менеджер юзера
@users_router.patch("/users/change_probation")
async def change_probation(user_id: int, new_probation: int, current_user: dict = Depends(verify_token),
                           db: Session = Depends(get_db)):
    manager_id = int(current_user.get("manager_id"))    # дістали айді менеджера
    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id.first()):
        query = update(Users).values(Probation=new_probation).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user are not an manager of a client!')
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.4 PATCH ендпоінт для зміни керівника юзера (може використовувати або менеджер, в якого level ролі < level-a ролі
# поточного менеджера, або сам поточний менеджер)
# наче працює, перевірити з суперюзером, створити його
@users_router.patch("/users/change_head_of_user")
async def change_head(user_id: int, new_head: int, current_user: dict = Depends(verify_token),
                      db: Session = Depends(get_db)):
    manager_id = int(current_user.get("manager_id"))  # дістали айді менеджера
    role_level_current_user = int(current_user.get("role_level"))
    role_level = db.query(Roles).join(Users).filter(Users.Id == user_id).first()
    role_level_user = role_level.Level
    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id).first() \
            or role_level_user < role_level_current_user:
        query = update(UsersManagers).values(ManagerId=new_head).where(UsersManagers.UserId == user_id)
        db.execute(query)
        db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user has no rights to change the manager')
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.5. GET ендпоінт для звільнення обраного юзера (в поле DismissalDate вноситься сьогоднішня дата), може
# використовувати менеджер користувача
@users_router.patch("/users/quit")
def quit_user(user_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    manager_id = int(current_user.get("manager_id"))  # дістали айді менеджера
    current_date = datetime.date.today()
    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id).first():
        query = update(Users).values(DismissalDate=current_date).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user are not an manager of a client!')
    return Response(status_code=status.HTTP_200_OK, description='User was successfully quited!')


# 2.6. PATCH ендпоінт для зміни ролі користувача (може використовувати менеджер користувача, або менеджер, в якого level
# ролі < level ролі поточного менеджера), level нової ролі користувача не може бути вище level-у ролі менеджера, який
# надіслав запит
@users_router.patch("/users/change_role")
def change_role(user_id: int, new_role: int,  current_user: dict = Depends(verify_token),
                db: Session = Depends(get_db)):
    manager_id = int(current_user.get("manager_id"))  # дістали айді менеджера
    role_level_current_user = int(current_user.get("role_level"))
    role_level = db.query(Roles).join(Users).filter(Users.Id == user_id).first()
    role_level_user = role_level.Level
    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id).first() \
            or role_level_user < role_level_current_user:
        query = update(Users).values(RoleId=new_role).where(Users.Id == user_id)
        db.execute(query)
        db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user are not an manager of a client!')
    return Response(status_code=status.HTTP_200_OK, description='Changed!')


# 2.7. DELETE ендпоінт для того, щоб прибрати користувача з підлеглих.
@users_router.delete("/users/delete_from_subordinates")
def delete_from_subordinates(user_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    manager_id = int(current_user.get("manager_id"))  # дістали айді менеджера
    if db.query(UsersManagers).filter(UsersManagers.ManagerId == manager_id, UsersManagers.UserId == user_id).first():
        row_to_delete = db.query(UsersManagers).filter(UsersManagers.UserId == user_id).first()
        if row_to_delete:
            db.delete(row_to_delete)
            db.commit()
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED,
                        description='The current user are not an manager of a client!')
    return Response(status_code=status.HTTP_200_OK, description='Deleted!')







