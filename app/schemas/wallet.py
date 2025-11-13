from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.models.wallet import WALLET_BALANCE_DEFAULT


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class WalletOperationRequest(BaseModel):
    operation_type: OperationType = Field(...)
    amount: int = Field(..., gt=0)


class WalletCreate(BaseModel):
    balance: Optional[int] = Field(ge=0, default=WALLET_BALANCE_DEFAULT)


class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    balance: int
