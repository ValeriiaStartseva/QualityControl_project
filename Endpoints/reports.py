from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from get_db import get_db
from sql_app.models import MonitoringScores
from Endpoints.filters import filter_for_reports

reports_router = APIRouter(prefix="/api/v0")


# 4.1
@reports_router.get("/monitoring/reports/full_report")
async def get_monitoring_full_report(start_date: date = None, end_date: date = None,
                                     r_number: int = None, manager_id: int = None,
                                     monitoring_manager_id: int = None, operator_id: int = None,
                                     type_of_call: bool = None, db: Session = Depends(get_db)):
    monitoring_records = filter_for_reports(start_date, end_date, r_number, manager_id, monitoring_manager_id,
                                            operator_id, type_of_call, db)
    monitoring_data_out = []
    for monitoring_record in monitoring_records:
        collect_login = monitoring_record.user.collect  # логін оператора
        contact_with = monitoring_record.contact
        result_call = monitoring_record.call_result
        type_of_call = monitoring_record.call_type
        discount = monitoring_record.discount
        collect_reestr = monitoring_record.contract.reestr
        user = monitoring_record.user.collect
        nks = monitoring_record.contract
        manager_ots = monitoring_record.manager.collect
        manager_sup = monitoring_record.user.manager.user.collect if monitoring_record.user.manager else None

        # count working days
        employment_date = monitoring_record.user.EmploymentDate
        dismissal_date = monitoring_record.user.DismissalDate
        if employment_date:
            if dismissal_date:
                delta = dismissal_date - employment_date
            else:
                delta = date.today() - employment_date
            years = delta.days // 365
            remaining_days = delta.days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            work_experience = f"{years} років {months} місяців {days} днів"
        list_total_score: list[MonitoringScores] = monitoring_record.monitoring_scores
        total_score = 0
        if list_total_score:
            for item in list_total_score:
                coefficient = item.score.Coefficient
                total_score += coefficient
        else:
            total_score = 0

        monitoring_data = {
            "Id моніторингу": monitoring_record.Id,
            "Логін оператора": collect_login.Login,
            "Стаж роботи оператора": work_experience,
            "ПІБ Оператора": user.FullName if user else None,
            "Id дзвінка": monitoring_record.CallId,
            "Телефон": monitoring_record.PhoneNumber,
            "Дата проведення оцінки": monitoring_record.MonitoringDate,
            "НКС": nks.Id if nks else None,
            "Реєстр": collect_reestr.RNumber if collect_reestr else None,
            "Контрагент": collect_reestr.Name if collect_reestr else None,
            "Сильні сторони": monitoring_record.Strong,
            "Слабкі сторони": monitoring_record.Weak,
            "Контакт з": contact_with.Name if contact_with else None,
            "Результат дзвінка": result_call.Name if result_call else None,
            "Тип дзвінка": type_of_call.Name if type_of_call else None,
            "Реструктуризація/дисконт": discount.Name if discount else None,
            "ПІБ оцінщика": manager_ots.FullName if manager_ots else None,
            "ПІБ супервізора": manager_sup.FullName if manager_sup else None,
            "Коментар": monitoring_record.Comment,
            "Проблема із дзвінком": 0,
            "Загальний бал": total_score,
        }
        monitoring_data_out.append(monitoring_data)

    return monitoring_data_out


# 4.2 не рахує середній бал та чомусь не вірно повертає імя для логіну оператора
@reports_router.get("/monitoring/reports/mean_score")
async def get_monitoring_report_mean_score(start_date: date = None, end_date: date = None,
                                           r_number: int = None, manager_id: int = None,
                                           monitoring_manager_id: int = None, operator_id: int = None,
                                           type_of_call: bool = None, db: Session = Depends(get_db)):
    monitoring_records = filter_for_reports(start_date, end_date, r_number, manager_id, monitoring_manager_id,
                                            operator_id, type_of_call, db)
    monitoring_data_out = []

    for monitoring_record in monitoring_records:
        collect_login = monitoring_record.user.collect   # логін оператора
        manager_sup = monitoring_record.user.manager.user.collect if monitoring_record.user.manager else None
        # count working days
        employment_date = monitoring_record.user.EmploymentDate
        dismissal_date = monitoring_record.user.DismissalDate
        if employment_date:
            if dismissal_date:
                delta = dismissal_date - employment_date
            else:
                delta = date.today() - employment_date
            years = delta.days // 365
            remaining_days = delta.days % 365
            months = remaining_days // 30
            days = remaining_days % 30
            work_experience = f"{years} років {months} місяців {days} днів"
        collect_full_name = monitoring_record.user.collect  # має бути ПІБ Оператора
        monitoring_data = {
                        "Логін оператора": collect_login.Login,
                        "ПІБ супервайзора": manager_sup.FullName if manager_sup else None,
                        "Стаж роботи оператора": work_experience,
                        "ПІБ Оператора": collect_full_name.FullName if collect_full_name else None,
                        "Кількість оцінених дзвінків": 0,
                        "Загальний середній бал": 0,
                    }

        monitoring_data_out.append(monitoring_data)

        monitoring_data_map = {}
        for monitoring in monitoring_data_out:
            login_operator = monitoring['Логін оператора']
            if login_operator not in monitoring_data_map:
                # якщо оператора ще немає в мапінгу, то додаємо його туди з його базовими даними
                monitoring_data_map[login_operator] = {
                    "Логін оператора": login_operator,
                    "ПІБ супервайзора": manager_sup.FullName if manager_sup else None,
                    "Стаж роботи оператора": work_experience,
                    "ПІБ Оператора": collect_full_name.FullName if collect_full_name else None,
                    "Кількість оцінених дзвінків": 0,
                    "Загальний середній бал": 0,
                }

            monitoring_data_map[login_operator]['Кількість оцінених дзвінків'] += 1
            monitoring_data_map[monitoring['Логін оператора']]['Загальний середній бал'] += monitoring['Загальний середній бал']

        # в кінці "розпаковуємо" мапінг в список, перетворюючи суму балів на середній бал
    return [
        {
            "Логін оператора": value["Логін оператора"],
            "ПІБ супервайзора": value["ПІБ супервайзора"],
            "Стаж роботи оператора": value["Стаж роботи оператора"],
            "ПІБ Оператора": value["ПІБ Оператора"],
            "Кількість оцінених дзвінків": value['Кількість оцінених дзвінків'],
            "Загальний середній бал": value['Загальний середній бал'] / value['Кількість оцінених дзвінків']
            # if
            # (value['Загальний середній бал'] is not None and value['Кількість оцінених дзвінків'] != 0) else 0
        } for value in monitoring_data_map.values()]




# варіант Жені

    #  monitoring_data_map = {}
    #
    #     for monitoring in monitoring_data_out:
    #         if monitoring['Логін оператора'] not in monitoring_data_map:
    #         # якщо оператора ще немає в мапінгу, то додаємо його туди з його базовими даними
    #             monitoring_data_map[monitoring['Логін оператора']] = monitoring
    #         # кількість оцінений дзвінків рахуємо тут, бо в query,
    #         #   яка "кількість оцінених дзвінків (не впевнена шо саме це треба рахувати???)"
    #         #   воно неправильно працює, ти там рахуєш кількість всіх моніторингів, а не тільки тих,
    #         #   які відповідають фільтрам, тому в тебе воно для всіх однакове буде
    #         monitoring_data_map['Кількість оцінених дзвінків'] = 0
    #     else:
    #         monitoring_data_map[monitoring['Логін оператора']]['Кількість оцінених дзвінків'] += 1
    #         # для кожного оператора сумуємо загальний середній бал
    #         monitoring_data_map[monitoring['Логін оператора']]['Загальний середній бал'] += monitoring[
    #             'Загальний середній бал']
    #
    #     # в кінці "розпаковуємо" мапінг в список, перетворючи суму балів на середній бал
    # return [
    #     {
    #         **value,
    #         'Загальний середній бал': value['Загальний середній бал'] / value['Кількість оцінених дзвінків']
    #     } for key, value in monitoring_data_map.items()
    # ]
