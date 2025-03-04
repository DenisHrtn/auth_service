import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

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
        sa.DateTime,
        nullable=False,
        default=func.now(),  # TODO: на уровне бд (server_default)
    )

    is_admin: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)

    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=False)

    is_blocked: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)

    date_joined: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, default=func.now()
    )


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
