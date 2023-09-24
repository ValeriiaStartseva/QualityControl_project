from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class CollectUser(Base):
    __tablename__ = 'CollectUser'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FullName = Column(String(45))
    Login = Column(String(45))
    IsManager = Column(String(45))
    Password = Column(String(45))
    IsDomain = Column(Integer)


class Monitoring(Base):
    __tablename__ = 'Monitoring'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CallId = Column(String(12))
    PhoneNumber = Column(String(11))
    MonitoringDate = Column(DateTime)
    ContractId = Column(Integer)
    Strong = Column(String(100))
    Weak = Column(String(100))
    ContactWithId = Column(Integer)
    CallResultId = Column(String(45))
    CallTypeId = Column(Integer)
    DiscountMarkId = Column(Integer)
    Comment = Column(String(45))
    ManagerId = Column(Integer, ForeignKey('Users.Id'))
    UserId = Column(Integer, ForeignKey('Users.Id'))
    ListType = Column(Integer)

    user = relationship('Users', lazy="selectin", foreign_keys=[UserId])
    manager = relationship('Users', lazy="selectin", foreign_keys=[ManagerId])


class MonitoringDictionary(Base):
    __tablename__ = 'MonitoringDictionary'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(45))
    Coefficient = Column(Integer)
    Description = Column(String(200))
    ListType = Column(Integer)


class MonitoringScores(Base):
    __tablename__ = 'MonitoringScores'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    MonitoringId = Column(Integer)
    ScoreTypeId = Column(Integer)


class Roles(Base):
    __tablename__ = 'Roles'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(45))
    Level = Column(Integer)


class Users(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserId = Column(Integer)
    RoteId = Column(Integer)
    EmploymentDate = Column(Date)
    DismissalDate = Column(Date)
    Email = Column(String(45))
    Probation = Column(Integer)
    Password = Column(String(50))



