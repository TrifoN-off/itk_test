import pytest
from httpx import AsyncClient

from app.schemas.wallet import OperationType
from tests.conftest import OPERATION_AMOUNT


@pytest.mark.asyncio
async def test_deposit_operation(client: AsyncClient, wallet: dict):
    """Тест для операции пополнения кошелька."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    operation_resp = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': OperationType.DEPOSIT,
            'amount': OPERATION_AMOUNT
        }
    )
    data = operation_resp.json()
    assert operation_resp.status_code == 200
    assert data.get('id') == wallet_id
    assert data.get('balance') == initial_balance + OPERATION_AMOUNT


@pytest.mark.asyncio
async def test_withdraw_operation(client: AsyncClient, wallet: dict):
    """Тест для операции снятия денег с кошелька."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    operation_response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': OperationType.WITHDRAW,
            'amount': OPERATION_AMOUNT
        }
    )
    data = operation_response.json()
    assert operation_response.status_code == 200
    assert data.get('id') == wallet_id
    assert data.get('balance') == initial_balance - OPERATION_AMOUNT


@pytest.mark.asyncio
async def test_withdraw_not_enough_balance(client: AsyncClient, wallet: dict):
    """Тест для операции снятия денег с кошелька с недостаточным балансом."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    operation_response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': OperationType.WITHDRAW,
            'amount': initial_balance + OPERATION_AMOUNT
        }
    )
    data = operation_response.json()
    assert operation_response.status_code == 400
    assert data.get('detail') == 'Not enough balance'


@pytest.mark.asyncio
async def test_invalid_operation_type(client: AsyncClient, wallet: dict):
    """Тест для неизвестного типа операции."""
    wallet_id = wallet.get('id')
    operation_response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={'operation_type': 'UNKNOWN', 'amount': OPERATION_AMOUNT}
    )
    assert operation_response.status_code == 422


@pytest.mark.asyncio
async def test_withdraw_with_negative_amount(
    client: AsyncClient,
    wallet: dict
):
    """Тест для снятия отрицательной суммы с кошелька."""
    wallet_id = wallet.get('id')
    operation_response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': OperationType.WITHDRAW,
            'amount': -OPERATION_AMOUNT
        }
    )
    assert operation_response.status_code == 422


@pytest.mark.asyncio
async def test_deposit_with_negative_amount(
    client: AsyncClient,
    wallet: dict
):
    """Тест для пополнения кошелька отрицательной суммой."""
    wallet_id = wallet.get('id')
    operation_response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': OperationType.DEPOSIT,
            'amount': -OPERATION_AMOUNT
        }
    )
    assert operation_response.status_code == 422
