from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String,  func, BigInteger, ForeignKey, Column, Integer, Table





class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


association_table = Table('user_group', Base.metadata,
            Column('user_id', Integer, ForeignKey('user.id')),
                    Column('group_id', Integer, ForeignKey('group.id')),
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, unique=True)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    users = relationship("User", secondary=association_table, backref="groups")

class Subject(Base):
    __tablename__ = 'subject'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id', ondelete='CASCADE'))

    group: Mapped['Group'] = relationship(backref='group')


class File(Base):
    __tablename__ = 'file'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    show_name: Mapped[str]= mapped_column(String(150), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    subject: Mapped['Subject'] = relationship(backref='subject')
    user: Mapped['User'] = relationship(backref='user')

