from fastapi import FastAPI, APIRouter
import sql_app.models as models
from sql_app.database import engine
from Endpoints.monitoring_dictionary_end import router as endpoint_router
from Endpoints.creating_new_users import router as endpoint_router_add_new_user
from Endpoints.authorization import login_router
from Endpoints.users_end import users_router
from Endpoints.contract import contract_router


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/api/v0")
router.include_router(endpoint_router_add_new_user)
router.include_router(endpoint_router)
router.include_router(login_router)
router.include_router(users_router)
router.include_router(contract_router)
app.include_router(router)





