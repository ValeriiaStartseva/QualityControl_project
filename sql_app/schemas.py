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
    ContractId: int
    Strong: str
    Weak: str
    ContactWithId: int
    CallResultId: int
    CallTypeId: int
    DiscountMarkId: int
    Comment: str
    UserId: int
    ListType: int
    list_with_id_md: list[int]


class MonitoringData(MonitoringBase):
    MonitoringDate: datetime
    ManagerId: int


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


class CollectReestr(BaseModelORM):
    Id: int | None = None
    RNumber: int
    Name: str
    ContractCnt: int
    ClientCnt: int
    CreationDat: date
    StartDate: date
    IsActual: int


class CollectContract(BaseModelORM):

    Id: int | None = None
    ReestrId: int
    ContractNum: str
    CurrencyId: int
    SummDelayBody: float
    SummDelayPercent: float
    SummDelayCommision:  float
    Fine: float
    SummToClose: float
    DelayStartDate: date
    ClientId: int



