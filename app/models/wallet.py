from datetime import datetime
import uuid

from sqlalchemy import UUID, CheckConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base

WALLET_BALANCE_DEFAULT = 2000   # Баланс по умолчанию
WALLET_BALANCE_MIN = 0          # Минимальный баланс


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    balance: Mapped[int] = mapped_column(
        nullable=False,
        default=WALLET_BALANCE_DEFAULT
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (CheckConstraint(
        f'balance >= {WALLET_BALANCE_MIN}', name='wallet_balance_non_negative'
    ),)

    def __repr__(self):
        return f'<Wallet(id={self.id}, balance={self.balance})>'
