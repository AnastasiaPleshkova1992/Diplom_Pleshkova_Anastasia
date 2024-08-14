from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[Optional[str]] = mapped_column(unique=True)
    password: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    other_name: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    birthday: Mapped[Optional[str]]
    city: Mapped[Optional[int]] = mapped_column(ForeignKey('cities.id'))
    additional_info: Mapped[Optional[str]]
    is_admin: Mapped[Optional[bool]] = mapped_column(default=False)


class City(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
