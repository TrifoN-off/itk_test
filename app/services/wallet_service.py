from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import WALLET_BALANCE_MIN, Wallet
from app.schemas.wallet import (
    WalletCreate,
    WalletOperationRequest,
    WalletResponse,
    OperationType,
)
from app.repositories.wallet_repository import WalletRepository


class WalletService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = WalletRepository(db)

    async def get_by_uuid(self, wallet_uuid: UUID) -> WalletResponse:
        """Получить кошелек по uuid."""
        wallet = await self.repository.get_by_uuid(wallet_uuid)
        if not wallet:
            raise HTTPException(status_code=404, detail='Wallet not found')
        return WalletResponse.model_validate(wallet)

    async def get_by_uuid_with_lock(
        self, wallet_uuid: UUID
    ) -> Wallet:
        """Получить кошелек по uuid с блокировкой."""
        wallet = await self.repository.get_by_uuid_with_lock(wallet_uuid)
        if not wallet:
            raise HTTPException(status_code=404, detail='Wallet not found')
        return wallet

    async def create(self, wallet_data: WalletCreate) -> WalletResponse:
        try:
            wallet = await self.repository.create(wallet_data)
            await self.db.commit()
            return WalletResponse.model_validate(wallet)
        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail='Internal server error'
            )

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
            raise HTTPException(
                status_code=500, detail='Internal server error'
            )

    def _calculate_new_balance(
        self, current_balance: int, operation_type: OperationType, amount: int
    ) -> int:
        """Расчета нового баланса кошелька."""
        if operation_type == OperationType.DEPOSIT:
            new_balance = current_balance + amount
        elif operation_type == OperationType.WITHDRAW:
            new_balance = current_balance - amount
        else:
            raise HTTPException(
                status_code=400, detail='Invalid operation type'
            )
        return new_balance

    def _validate_balance(self, balance: int):
        """Валидация баланса кошелька."""
        if balance < WALLET_BALANCE_MIN:
            raise HTTPException(
                status_code=400, detail='Not enough balance'
            )
