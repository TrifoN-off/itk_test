from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.wallet import (
    WalletCreate,
    WalletOperationRequest,
    WalletResponse,
)
from app.services.wallet_service import WalletService


router = APIRouter(
    prefix='/wallets',
    tags=['Wallets']
)


@router.get(
    '/{wallet_uuid}',
    response_model=WalletResponse,
    status_code=status.HTTP_200_OK
)
async def get_wallet(
    wallet_uuid: UUID,
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    """Получить информацию о кошельке."""
    return await WalletService(db).get_by_uuid(wallet_uuid)


@router.post(
    '',
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_wallet(
    wallet_data: WalletCreate = Depends(),
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    """Создать кошелек."""
    return await WalletService(db).create(wallet_data)


@router.post(
    '/{wallet_uuid}/operation',
    response_model=WalletResponse,
    status_code=status.HTTP_200_OK
)
async def update_wallet_balance(
    wallet_uuid: UUID,
    wallet_request: WalletOperationRequest = Depends(),
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    """Обновить баланс кошелька."""
    return await WalletService(db).update_balance(wallet_request, wallet_uuid)
