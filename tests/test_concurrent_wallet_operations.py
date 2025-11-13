import asyncio
import random

import pytest
from httpx import AsyncClient

from app.schemas.wallet import OperationType
from tests.conftest import (CONCURRENT_OPERATIONS_COUNT,
                            DEPOSIT_OPERATIONS_COUNT, OPERATION_AMOUNT,
                            WITHDRAW_OPERATIONS_COUNT)


@pytest.mark.asyncio
async def test_concurrent_deposits(client: AsyncClient, wallet: dict):
    """Тест для параллельных операций пополнения кошелька."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    tasks = [
        client.post(
            f'/api/v1/wallets/{wallet_id}/operation',
            json={
                'operation_type': OperationType.DEPOSIT,
                'amount': OPERATION_AMOUNT,
            },
        )
        for _ in range(CONCURRENT_OPERATIONS_COUNT)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(response.status_code == 200 for response in responses)
    final_response = await client.get(f'/api/v1/wallets/{wallet_id}')
    data = final_response.json()
    expected_balance = initial_balance + (
        OPERATION_AMOUNT * CONCURRENT_OPERATIONS_COUNT
    )
    assert data.get('id') == wallet_id
    assert data.get('balance') == expected_balance


@pytest.mark.asyncio
async def test_concurrent_withdrawals(client: AsyncClient, wallet: dict):
    """Тест для параллельных операций снятия денег с кошелька."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    tasks = [
        client.post(
            f'/api/v1/wallets/{wallet_id}/operation',
            json={
                'operation_type': OperationType.WITHDRAW,
                'amount': OPERATION_AMOUNT
            }
        )
        for _ in range(CONCURRENT_OPERATIONS_COUNT)
    ]
    responses = await asyncio.gather(*tasks)
    assert all(response.status_code == 200 for response in responses)
    final_response = await client.get(f'/api/v1/wallets/{wallet_id}')
    data = final_response.json()
    expected_balance = initial_balance - (
        OPERATION_AMOUNT * CONCURRENT_OPERATIONS_COUNT
    )
    assert data.get('id') == wallet_id
    assert data.get('balance') == expected_balance


@pytest.mark.asyncio
async def test_concurrent_mixed_operations(client: AsyncClient, wallet: dict):
    """Тест для параллельных операций снятия и пополнения кошелька."""
    wallet_id = wallet.get('id')
    initial_balance = wallet.get('balance')
    tasks = []
    for _ in range(DEPOSIT_OPERATIONS_COUNT):
        tasks.append(
            client.post(
                f'/api/v1/wallets/{wallet_id}/operation',
                json={
                    'operation_type': OperationType.DEPOSIT,
                    'amount': OPERATION_AMOUNT
                }
            )
        )
    for _ in range(WITHDRAW_OPERATIONS_COUNT):
        tasks.append(
            client.post(
                f'/api/v1/wallets/{wallet_id}/operation',
                json={
                    'operation_type': OperationType.WITHDRAW,
                    'amount': OPERATION_AMOUNT
                }
            )
        )
    random.shuffle(tasks)
    responses = await asyncio.gather(*tasks)
    assert all(response.status_code == 200 for response in responses)
    final_response = await client.get(f'/api/v1/wallets/{wallet_id}')
    data = final_response.json()
    expected_balance = (
        initial_balance
        + (DEPOSIT_OPERATIONS_COUNT * OPERATION_AMOUNT)
        - (WITHDRAW_OPERATIONS_COUNT * OPERATION_AMOUNT)
    )
    assert data.get('id') == wallet_id
    assert data.get('balance') == expected_balance
