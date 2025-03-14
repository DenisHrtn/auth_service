import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.repos.sqla.base import Base


class UserModel(Base):
    """
    Модель пользователей
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)

    username: Mapped[str] = mapped_column(sa.String(255), unique=True)

    hashed_password: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    code: Mapped[int] = mapped_column(sa.Integer, nullable=False, unique=True)

    code_created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    is_admin: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)

    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=False)

    is_blocked: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)

    date_joined: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, default=text("CURRENT_TIMESTAMP")
    )

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", uselist=False
    )

    role: Mapped["Role"] = relationship("Role", back_populates="user", uselist=False)


class Profile(Base):
    """
    Модель профиля
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(sa.String(255), nullable=False, default="")

    last_name: Mapped[str] = mapped_column(sa.String(255), nullable=False, default="")

    info: Mapped[str] = mapped_column(sa.String(255), nullable=False, default="")

    speciality: Mapped[str] = mapped_column(
        sa.String(255), nullable=False, default="Programmer"
    )

    days_with_service: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")


class Role(Base):
    """
    Модель ролей
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    role_name: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)

    description: Mapped[str] = mapped_column(sa.Text, nullable=False)

    permissions: Mapped[list[int]] = mapped_column(ARRAY(sa.Integer), nullable=False)

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", name="role_user_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("UserModel", backref="roles", lazy="joined")


class TagChoices(enum.Enum):
    CREATOR = "creator"
    EDITOR = "editor"
    VIEWER = "viewer"
    DELETER = "deleter"
    ADMIN = "admin"


class Permission(Base):
    """
    Модель разрешений
    """

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)

    permission_name: Mapped[str] = mapped_column(
        sa.String(255), unique=True, nullable=False
    )

    description: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    tag: Mapped[TagChoices] = mapped_column(
        sa.Enum(TagChoices, name="tag_choices"),
        nullable=False,
        default=TagChoices.VIEWER,
    )
