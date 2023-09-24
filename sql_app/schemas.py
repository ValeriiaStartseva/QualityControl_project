from pydantic import Field

from sql_app.base_model import BaseModelORM
from datetime import datetime, date


class CollectUserBase(BaseModelORM):
    Id: int
    FullName: str
    Login: str
    IsManager: str
    Password: str
    IsDomain: int


class MonitoringBase(BaseModelORM):
    Id: int
    CallId: str
    PhoneNumber: str
    MonitoringDate: datetime
    ContractId: int
    Strong: str
    Weak: str
    ContactWithId: int
    CallResultId: str
    CallTypeId: int
    DiscountMarkId: int
    Comment: str
    ManagerId: int
    UserId: int
    ListType: int


class MonitoringDictionaryBase(BaseModelORM):
    Id: int | None = Field(None, description='gfhudefj')
    Name: str
    Coefficient: int
    Description: str | None
    ListType: int


class MonitoringScoresBase(BaseModelORM):
    Id: int
    MonitoringId: int
    ScoreTypeId: int


class RolesBase(BaseModelORM):
    Id: int
    Name: str
    Level: int


class UsersBase(BaseModelORM):
    Id: int
    UserId: int
    RoteId: int
    EmploymentDate: date
    DismissalDate: date
    Email: str
    Probation: int
    Password: str

