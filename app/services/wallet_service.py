from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import WALLET_BALANCE_MIN, Wallet
from app.repositories.wallet_repository import WalletRepository
from app.schemas.wallet import (OperationType, WalletCreate,
                                WalletOperationRequest, WalletResponse)


class WalletService:
    """Сервис для работы с кошельками."""
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = WalletRepository(db)

    async def get_by_uuid(self, wallet_uuid: UUID) -> WalletResponse:
        """Получить кошелек по uuid."""
        try:
            wallet = await self.repository.get_by_uuid(wallet_uuid)
            if not wallet:
                raise HTTPException(status_code=404, detail='Wallet not found')
            return WalletResponse.model_validate(wallet)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500)

    async def get_by_uuid_with_lock(
        self, wallet_uuid: UUID
    ) -> Wallet:
        """Получить кошелек по uuid с блокировкой."""
        try:
            wallet = await self.repository.get_by_uuid_with_lock(wallet_uuid)
            if not wallet:
                raise HTTPException(status_code=404, detail='Wallet not found')
            return wallet
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500)

    async def create(self, wallet_data: WalletCreate) -> WalletResponse:
        """Создать кошелек."""
        try:
            wallet = await self.repository.create(wallet_data)
            await self.db.commit()
            return WalletResponse.model_validate(wallet)
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500)

    async def update_balance(
        self, wallet_request: WalletOperationRequest, wallet_uuid: UUID
    ) -> WalletResponse:
        """Обновить баланс кошелька."""
        try:
            wallet = await self.get_by_uuid_with_lock(wallet_uuid)
            new_balance = self._calculate_new_balance(
                wallet.balance,
                wallet_request.operation_type,
                wallet_request.amount
            )
            self._validate_balance(new_balance)
            wallet = await self.repository.update_balance(wallet, new_balance)
            await self.db.commit()
            return WalletResponse.model_validate(wallet)
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception:
            await self.db.rollback()
            raise HTTPException(status_code=500)

    def _calculate_new_balance(
        self, current_balance: int, operation_type: OperationType, amount: int
    ) -> int:
        """Расчета нового баланса кошелька."""
        if operation_type == OperationType.DEPOSIT:
            new_balance = current_balance + amount
        elif operation_type == OperationType.WITHDRAW:
            new_balance = current_balance - amount
        return new_balance

    def _validate_balance(self, balance: int):
        """Валидация баланса кошелька."""
        if balance < WALLET_BALANCE_MIN:
            raise HTTPException(
                status_code=400, detail='Not enough balance'
            )
