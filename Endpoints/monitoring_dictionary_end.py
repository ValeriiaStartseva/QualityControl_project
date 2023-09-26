from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from sqlalchemy import update
from sqlalchemy.orm import Session
from starlette import status

from get_db import get_db
from sql_app.schemas import MonitoringDictionaryBase
from sql_app.models import MonitoringDictionary

router = APIRouter(prefix="/api/v0")


@router.get("/monitoring_dictionary/{list_type}", response_model=list[MonitoringDictionaryBase])
async def get_md_by_list_type(list_type: int, db: Session = Depends(get_db)):
    monitoring_dictionary: list[MonitoringDictionary] = db.query(MonitoringDictionary).filter(
        MonitoringDictionary.ListType == list_type).all()
    return [MonitoringDictionaryBase.model_validate(model) for model in monitoring_dictionary]


@router.post("/monitoring_dictionary/add_new_monitoring_points")
async def add_new_monitoring_points(monitoring_points: MonitoringDictionaryBase, db: Session = Depends(get_db)):
    monitoring_points_record = MonitoringDictionary(**monitoring_points.model_dump(exclude={'Id'}))
    db.add(monitoring_points_record)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED, description='Added!')


@router.patch("/monitoring_dictionary/change_monitoring_points/{Id}")
async def change_monitoring_name(name_id: int, name: str, db: Session = Depends(get_db)):
    query = update(MonitoringDictionary).values(Name=name).where(MonitoringDictionary.Id == name_id)
    db.execute(query)
    db.commit()
    return Response(status_code=status.HTTP_200_OK, description='Changed!')
