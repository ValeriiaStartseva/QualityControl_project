from fastapi import FastAPI, APIRouter
import sql_app.models as models
from sql_app.database import engine
from Endpoints.monitoring_dictionary_end import router as endpoint_router


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/api/v0")
router.include_router(endpoint_router)
app.include_router(router)


# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UsersBase, db: db_dependency):
#     db_user = models.Users(**user.model_dump())
#     db.add(db_user)
#     db.commit()

