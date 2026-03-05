from sqlalchemy import Column, Integer, String, BigInteger
from database.db import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(100))
    full_name = Column(String(100))
    role = Column(String(20), default="student")
