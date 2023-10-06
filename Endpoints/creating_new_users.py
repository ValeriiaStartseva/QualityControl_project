from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status
from get_db import get_db
from sql_app.schemas import RolesBase, UsersBase, UserIn,  CollectUserBase
from sql_app.models import Roles, Users, CollectUser, UsersManagers
from Endpoints.hashing import hash_password

router = APIRouter(prefix="/api/v0")


@router.get("/collect_users", response_model=list[CollectUserBase])
async def get_collect_users(db: Session = Depends(get_db)):
    collect_user = db.query(CollectUser).all()
    return [CollectUserBase.model_validate(model) for model in collect_user]


@router.get("/roles", response_model=list[RolesBase])
async def get_roles_by_id(db: Session = Depends(get_db)):
    role = db.query(Roles).all()
    return [RolesBase.model_validate(model) for model in role]


@router.get("/users/managers", response_model=list[UsersBase])
async def get_true_boss(db: Session = Depends(get_db)):
    users_dictionary = db.query(Users).filter(Users.RoleId < 2, Users.DismissalDate.is_(None)).all()
    return [UsersBase.model_validate(model) for model in users_dictionary]


@router.post("/create_user")
async def add_new_user(user_points: UserIn, db: Session = Depends(get_db)):
    hashed_password = hash_password(user_points.Password)
    user_points_record = Users(UserId=user_points.UserId, RoleId=user_points.RoleId,
                               EmploymentDate=user_points.EmploymentDate, DismissalDate=user_points.DismissalDate,
                               Email=user_points.Email, Probation=user_points.Probation, Password=hashed_password)
    # user_points_record = Users(**user_points.model_dump(exclude={'Id', 'ManagerId'}))
    db.add(user_points_record)
    db.flush()
    last_row = db.query(Users).order_by(Users.Id.desc()).first()
    data = {
        'UserId': last_row.Id,
        'ManagerId': user_points.ManagerId
    }
    manager_points_record = UsersManagers(**data)
    db.add(manager_points_record)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED, description='Added!')
