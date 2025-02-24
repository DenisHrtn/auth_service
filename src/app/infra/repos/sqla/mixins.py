from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class TimestampMixin:
    timestamp = Annotated[
        datetime, mapped_column(nullable=False, default=datetime.utcnow)
    ]

    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp] = mapped_column(
        onupdate=datetime.utcnow,
    )
