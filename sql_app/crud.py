from sqlalchemy.orm import Session
import sql_app.models as models


def get_monitoring_dictionary(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MonitoringDictionary).offset(skip).limit(limit).all()


def get_monitoring_dictionary_list_type(db: Session, list_type: int):
    return db.query(models.MonitoringDictionary).filter(models.MonitoringDictionary.ListType == list_type).all()





