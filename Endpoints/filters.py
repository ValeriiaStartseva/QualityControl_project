from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from get_db import get_db
from sql_app.models import CollectContract, CollectReestr, Monitoring, BasicDictionary, MonitoringScores
from sqlalchemy import and_
from Endpoints.authorization import verify_token
from fastapi.openapi.models import Response
from starlette import status
from sql_app.schemas import MonitoringBase
from typing import Literal


def filter_monitoring_record1(start_date: date = None,
                              end_date: date = None,
                              id_operator: int = None,
                              id_otsinshik: int = None,
                              db: Session = Depends(get_db)):
    base_query = db.query(Monitoring)
    filter_conditions = []

    if start_date and end_date:
        filter_conditions.append(and_(Monitoring.MonitoringDate >= start_date, Monitoring.MonitoringDate <= end_date))
    if id_operator:
        filter_conditions.append(Monitoring.UserId == id_operator)
    if id_otsinshik:
        filter_conditions.append(Monitoring.ManagerId == id_otsinshik)

    if filter_conditions:
        combined_filter = and_(*filter_conditions)
        base_query = base_query.filter(combined_filter)

    monitoring_records = base_query.all()
    return monitoring_records


def filter_for_reports(start_date: date = None,
                       end_date: date = None,
                       r_number: int = None,
                       manager_id: int = None,
                       monitoring_manager_id: int = None,
                       operator_id: int = None,
                       type_of_call: bool = None,
                       db: Session = Depends(get_db)):
    base_query = db.query(Monitoring)
    filter_conditions = []
    if start_date and end_date:  # monitoring_date, Monitoring.MonitoringDate
        filter_conditions.append(and_(Monitoring.MonitoringDate >= start_date, Monitoring.MonitoringDate <= end_date))
    if r_number:  # reestr number,  CollectReestr.RNumber
        filter_conditions.append(Monitoring.contract.reestr.RNumber == r_number)
    if manager_id:  # UsersManagers.ManagerId
        filter_conditions.append(Monitoring.user.manager.ManagerId == manager_id)
    if monitoring_manager_id:  # Monitoring.ManagerId
        filter_conditions.append(Monitoring.ManagerId == monitoring_manager_id)
    if operator_id:  # Monitoring.UserId
        filter_conditions.append(Monitoring.UserId == operator_id)
    if type_of_call is True:
        filter_conditions.append(Monitoring.CallId == "тест")
    if type_of_call is False:
        filter_conditions.append(Monitoring.CallId != "тест")
    if filter_conditions:
        combined_filter = and_(*filter_conditions)
        base_query = base_query.filter(combined_filter)
    monitoring_records = base_query.all()
    return monitoring_records
