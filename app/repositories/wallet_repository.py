from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate


class WalletRepository:
    """Репозиторий для работы с кошельками."""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, wallet_data: WalletCreate) -> Wallet:
        """Создать новый кошелек."""
        db_wallet = Wallet(**wallet_data.model_dump())
        self.db.add(db_wallet)
        await self.db.flush()
        await self.db.refresh(db_wallet)
        return db_wallet

    async def get_by_uuid(self, wallet_uuid: UUID) -> Optional[Wallet]:
        """Получить кошелек по uuid."""
        result = await self.db.execute(
            select(Wallet).where(Wallet.id == wallet_uuid)
        )
        return result.scalars().first()

    async def get_by_uuid_with_lock(
        self, wallet_uuid: UUID
    ) -> Optional[Wallet]:
        """
        Получить кошелек по uuid с блокировкой.
        Необходимо для правильной обработки конкурентных операций.
        """
        result = await self.db.execute(
            select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
        )
        return result.scalars().first()

    async def update_balance(self, wallet: Wallet, new_balance: int) -> Wallet:
        """Обновить баланс кошелька."""
        wallet.balance = new_balance
        await self.db.flush()
        await self.db.refresh(wallet)
        return wallet
