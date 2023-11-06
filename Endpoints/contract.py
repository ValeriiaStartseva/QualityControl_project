import datetime
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

contract_router = APIRouter(prefix="/api/v0")


# 3.1
@contract_router.get("/amount_of_owed")
async def get_amount_of_owed_by_contract_id(contract_id: int, db: Session = Depends(get_db)):
    query = db.query(CollectContract).\
        join(CollectReestr, and_(CollectContract.ReestrId == CollectReestr.Id)).\
        filter(CollectContract.Id == contract_id)

    data = []
    for query in query:
        data.append({
            "Сума боргу": query.SummToClose,
            "Номер реєстру": query.reestr.RNumber,
            "Назва реєстру": query.reestr.Name,
        })
    return data


# 3.2
@contract_router.get("/basic_dictionary")
async def basic_dictionary(type_dictionary: Literal["контакт з", "результат дзвінка", "дисконт", "реструктуризація",
                                                    "тип дзвінка"],
                           result_with_contact: int = None, db: Session = Depends(get_db)):
    query = db.query(BasicDictionary)
    if "контакт з" in type_dictionary:
        query = query.filter(BasicDictionary.Specid == 2)
    if "результат дзвінка" in type_dictionary:
        if result_with_contact in [3, 4]:  # Должник | Поручитель
            query = query.filter(BasicDictionary.Specid.in_([3, 4]))
        if result_with_contact in [5, 6]:  # Родственник | Третье лицо
            query = query.filter(BasicDictionary.Specid.in_([4, 5]))
    if "дисконт" in type_dictionary or "реструктуризація" in type_dictionary:
        query = query.filter(BasicDictionary.Specid == 1)
    if "тип дзвінка" in type_dictionary:
        query = query.filter(BasicDictionary.Specid == 6)

    items = query.all()
    data = []
    for item in items:
        data.append({
            "Id": item.Id,
            "Name": item.Name,
        })
    return data


# 3.3 & 3.4
@contract_router.post("/monitoring/add_new_monitoring_points")
async def add_new_monitoring_points(monitoring_points: MonitoringBase, db: Session = Depends(get_db),
                                    current_user: dict = Depends(verify_token)):
    manager_id = int(current_user["manager_id"])  # Get the manager's ID
    current_date = datetime.date.today()    # Get the date
    monitoring_data = {
        "CallId": monitoring_points.CallId,
        "PhoneNumber": monitoring_points.PhoneNumber,
        "ContractId": monitoring_points.ContractId,
        "Strong": monitoring_points.Strong,
        "Weak": monitoring_points.Weak,
        "ContactWithId": monitoring_points.ContactWithId,
        "CallResultId": monitoring_points.CallResultId,
        "CallTypeId": monitoring_points.CallTypeId,
        "DiscountMarkId": monitoring_points.DiscountMarkId,
        "Comment": monitoring_points.Comment,
        "UserId": monitoring_points.UserId,
        "ListType": monitoring_points.ListType,
        "ManagerId": manager_id,
        "MonitoringDate": current_date,
    }
    monitoring_data_record = Monitoring(**monitoring_data)    # add new row to Monitoring Table
    db.add(monitoring_data_record)
    db.flush()

    last_row = db.query(Monitoring).order_by(Monitoring.Id.desc()).first()
    response = last_row.Id  # id of row for response
    for item in range(len(monitoring_points.list_with_id_md)):
        monitoring_scores_data = {      # dict for add to MonitoringScores table
            "MonitoringId": last_row.Id,
            "ScoreTypeId": monitoring_points.list_with_id_md[item],
        }
        monitoring_scores_data_record = MonitoringScores(**monitoring_scores_data)
        db.add(monitoring_scores_data_record)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED, description=f'Added new row with id {response}')


# 3.5 & 3.6
@contract_router.get("/monitoring")
def data_from_monitoring(start_date: datetime.date = None,
                         end_date: datetime.date = None,
                         id_operator: int = None,
                         id_otsinshik: int = None,
                         db: Session = Depends(get_db)):

    # filtering
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

    monitoring_data_out = []

    for monitoring_record in monitoring_records:
        contact_with = monitoring_record.contact
        result_call = monitoring_record.call_result
        type_of_call = monitoring_record.call_type
        discount = monitoring_record.discount
        collect_reestr = monitoring_record.contract.reestr
        user = monitoring_record.user.collect
        nks = monitoring_record.contract
        manager_ots = monitoring_record.manager.collect
        manager_sup = monitoring_record.user.manager.user.collect if monitoring_record.user.manager else None
        list_total_score: list[MonitoringScores] = monitoring_record.monitoring_scores
        total_score = 0
        if list_total_score:
            for item in list_total_score:
                coefficient = item.score.Coefficient
                total_score += coefficient
        else:
            total_score = 0

        monitoring_data = {
            "Дата проведення оцінки": monitoring_record.MonitoringDate,
            "ПІБ оператора": user.FullName if user else None,
            "Id дзвінка": monitoring_record.CallId,
            "Телефон": monitoring_record.PhoneNumber,
            "Контрагент": collect_reestr.Name if collect_reestr else None,
            "Реєстр": collect_reestr.RNumber if collect_reestr else None,
            "НКС": nks.Id if nks else None,
            "Сильні сторони": monitoring_record.Strong,
            "Слабкі сторони": monitoring_record.Weak,
            "Контакт з": contact_with.Name if contact_with else None,
            "Результат дзвінка": result_call.Name if result_call else None,
            "Тип дзвінка": type_of_call.Name if type_of_call else None,
            "Реструктуризація/Дисконт": discount.Name if discount else None,
            "ПІБ оцінщика": manager_ots.FullName if manager_ots else None,
            "ПІБ супервізора": manager_sup.FullName if manager_sup else None,
            "Коментар": monitoring_record.Comment,
            "Загальний бал": total_score,
        }

        monitoring_data_out.append(monitoring_data)
    return monitoring_data_out

