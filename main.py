from fastapi import FastAPI, APIRouter
import sql_app.models as models
from sql_app.database import engine
from Endpoints.monitoring_dictionary_end import router as endpoint_router
from Endpoints.creating_new_users import router as endpoint_router_add_new_user


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


router = APIRouter(prefix="/api/v0")
router.include_router(endpoint_router_add_new_user)
router.include_router(endpoint_router)
app.include_router(router)





