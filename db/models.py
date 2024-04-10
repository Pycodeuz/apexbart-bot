import re
from enum import Enum

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import TypeDecorator

from db.base import Base


class ExamStatus(Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    PENDING = "Pending"


class ExamStatusType(TypeDecorator):
    impl = String

    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class(value)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    tg_id = Column(String, unique=True, index=True)
    lang_level = Column(String)
    login_code = Column(String, unique=True, index=True)
    exam_status = Column(ExamStatusType(ExamStatus), default=ExamStatus.PENDING)
    task_completion = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="users")


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    requirements = Column(String)
    start_date = Column(DateTime)
    login_codes = Column(ARRAY(String), nullable=False)
    users = relationship("User", back_populates="project")

    @validates('login_codes')
    def validate_login_codes(self, key, login_codes):
        # Check if all codes are unique
        if len(login_codes) != len(set(login_codes)):
            raise ValueError("Login codes must be unique")

        # Check if each code is 5 or 6 digits
        for code in login_codes:
            if not re.match(r'^\d{5,6}$', code):
                raise ValueError("Each login code must be 5 or 6 digits")

        return login_codes


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tg_id = Column(String)
