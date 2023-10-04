from pydantic import Field
from sql_app.base_model import BaseModelORM
from datetime import datetime, date


class CollectUserBase(BaseModelORM):
    Id: int | None = None
    FullName: str
    Login: str


class CollectUserDetails(CollectUserBase):
    IsManager: str
    Password: str
    IsDomain: int


class UsersManagersBase(BaseModelORM):
    Id: int | None = None
    ManagerId: int
    UserId: int


class MonitoringBase(BaseModelORM):
    Id: int | None = None
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
    Description: str | None = None
    ListType: int


class MonitoringScoresBase(BaseModelORM):
    Id: int
    MonitoringId: int
    ScoreTypeId: int


class RolesBase(BaseModelORM):
    Id: int | None = None
    Name: str


class RoleBase(RolesBase):
    Level: int


class UsersBase(BaseModelORM):
    Id: int | None = None
    UserId: int
    RoleId: int
    EmploymentDate: date
    DismissalDate: date | None = None
    Email: str
    Probation: int


class UserIn(UsersBase):
    Password: str
    ManagerId: int


class UserOut(UsersBase):
    pass



