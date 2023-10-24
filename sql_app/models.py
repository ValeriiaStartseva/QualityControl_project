from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float
from .database import Base
from sqlalchemy.orm import relationship


class BasicDictionary(Base):
    __tablename__ = 'BasicDictionary'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(400))
    Description = Column(String(400))
    Code = Column(String(400))
    Specid = Column(Integer)


class Roles(Base):
    __tablename__ = 'Roles'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(400))
    Level = Column(Integer)


class CollectUser(Base):
    __tablename__ = 'CollectUser'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FullName = Column(String(400))
    Login = Column(String(400))
    IsManager = Column(String(400))
    Password = Column(String(400))
    IsDomain = Column(Integer)


class UsersManagers(Base):
    __tablename__ = 'UsersManagers'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ManagerId = Column(Integer, ForeignKey('Users.Id'))
    UserId = Column(Integer, ForeignKey('Users.Id'))

    user = relationship('Users', lazy="selectin", foreign_keys=[UserId])
    manager = relationship('Users', lazy="selectin", foreign_keys=[ManagerId])


class Monitoring(Base):
    __tablename__ = 'Monitoring'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CallId = Column(String(400))
    PhoneNumber = Column(String(400))
    MonitoringDate = Column(DateTime)
    ContractId = Column(Integer, ForeignKey('CollectContract.Id'))
    Strong = Column(String(400))
    Weak = Column(String(400))
    ContactWithId = Column(Integer, ForeignKey('BasicDictionary.Id'))
    CallResultId = Column(Integer, ForeignKey('BasicDictionary.Id'))
    CallTypeId = Column(Integer, ForeignKey('BasicDictionary.Id'))
    DiscountMarkId = Column(Integer, ForeignKey('BasicDictionary.Id'))
    Comment = Column(String(400))
    ManagerId = Column(Integer, ForeignKey('Users.Id'))
    UserId = Column(Integer, ForeignKey('Users.Id'))
    ListType = Column(Integer)

    user = relationship('Users', lazy="selectin", foreign_keys=[UserId])
    manager = relationship('Users', lazy="selectin", foreign_keys=[ManagerId])
    contact = relationship('BasicDictionary', lazy="selectin", foreign_keys=[ContactWithId])
    call_result = relationship('BasicDictionary', lazy="selectin", foreign_keys=[CallResultId])
    call_type = relationship('BasicDictionary', lazy="selectin", foreign_keys=[CallTypeId])
    contract = relationship('CollectContract', lazy="selectin", foreign_keys=[ContractId])
    discount = relationship('BasicDictionary', lazy="selectin", foreign_keys=[DiscountMarkId])


class MonitoringDictionary(Base):
    __tablename__ = 'MonitoringDictionary'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(400))
    Coefficient = Column(Integer)
    Description = Column(String(400))
    ListType = Column(Integer)


class MonitoringScores(Base):
    __tablename__ = 'MonitoringScores'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    MonitoringId = Column(Integer, ForeignKey('Monitoring.Id'))
    ScoreTypeId = Column(Integer,  ForeignKey('MonitoringDictionary.Id'))

    monitoring = relationship('Monitoring', lazy="selectin", foreign_keys=[MonitoringId])
    scope = relationship('MonitoringDictionary', lazy="selectin", foreign_keys=[ScoreTypeId])


class Users(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserId = Column(Integer,  ForeignKey('CollectUser.Id'),)
    RoleId = Column(Integer,  ForeignKey('Roles.Id'))
    EmploymentDate = Column(Date)
    DismissalDate = Column(Date)
    Email = Column(String(400))
    Probation = Column(Integer)
    Password = Column(String(400))

    collect = relationship('CollectUser', lazy="selectin", foreign_keys=[UserId])
    role = relationship('Roles', lazy="selectin", foreign_keys=[RoleId])


class CollectReestr(Base):
    __tablename__ = 'CollectReestr'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    RNumber = Column(Integer)
    Name = Column(String(400))
    ContractCnt = Column(Integer)
    ClientCnt = Column(Integer)
    CreationDate = Column(Date)
    StartDate = Column(Date)
    IsActual = Column(Integer)


class CollectContract(Base):
    __tablename__ = 'CollectContract'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ReestrId = Column(Integer, ForeignKey('CollectReestr.Id'))
    ContractNum = Column(String(400))
    CurrencyId = Column(Integer)
    SummDelayBody = Column(Float)
    SummDelayPercent = Column(Float)
    SummDelayCommision = Column(Float)
    Fine = Column(Float)
    SummToClose = Column(Float)
    DelayStartDate = Column(Date)
    ClientId = Column(Integer)

    reestr = relationship('CollectReestr', lazy="selectin", foreign_keys=[ReestrId])
