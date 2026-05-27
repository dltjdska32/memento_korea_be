from datetime import datetime

from sqlalchemy import func, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Base 엔터티
class Base(DeclarativeBase):

    # 생성일
    created_at = Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), # insert 시 자동설정
        nullable = False
    )

    updated_at = Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),        # 수정시 자동 갱신
        nullable = False
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        nullable = False
    )