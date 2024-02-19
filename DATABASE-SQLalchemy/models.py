from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, select, Text, and_, desc, func, Column
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship, as_declarative
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable = False)


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key = True)
    name = Column(Text, nullable = False)
    group_id = Column(Integer, ForeignKey(Groups.id, ondelete="CASCADE"))


class Lectors(Base):
    __tablename__ = 'lectors'
    id = Column(Integer, primary_key = True)
    name = Column(Text, nullable = False)


class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key = True)
    name = Column(Text, nullable = False)
    lector_id = Column(Integer, ForeignKey(Lectors.id, ondelete="CASCADE"))


class Marks(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key = True)
    value = Column(Integer, nullable = False)
    timestamp = Column(Text)
    subject_id = Column(Integer, ForeignKey(Subjects.id, ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey(Students.id, ondelete="CASCADE"))
    

