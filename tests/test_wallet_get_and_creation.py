from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from app.models.wallet import WALLET_BALANCE_DEFAULT
from tests.conftest import CUSTOM_BALANCE


@pytest.mark.asyncio
async def test_create_wallet_default_balance(client: AsyncClient):
    """Тест для создания кошелька с дефолтным балансом."""
    response = await client.post('/api/v1/wallets', json={})
    data = response.json()
    assert response.status_code == 201
    assert UUID(data.get('id'))
    assert data.get('balance') == WALLET_BALANCE_DEFAULT


@pytest.mark.asyncio
async def test_create_wallet_custom_balance(client: AsyncClient):
    """Тест для создания кошелька с заданым балансом."""
    response = await client.post(
        '/api/v1/wallets',
        json={'balance': CUSTOM_BALANCE}
    )
    data = response.json()
    assert response.status_code == 201
    assert data.get('balance') == CUSTOM_BALANCE


@pytest.mark.asyncio
async def test_create_wallet_negative_custom_balance(client: AsyncClient):
    """Тест для создания кошелька с отрицательным балансом."""
    response = await client.post(
        '/api/v1/wallets',
        json={'balance': -CUSTOM_BALANCE}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_wallet(client: AsyncClient):
    """Тест для получения информации о кошельке."""
    create_response = await client.post('/api/v1/wallets', json={})
    wallet_data = create_response.json()
    wallet_id = wallet_data.get('id')
    get_response = await client.get(f'/api/v1/wallets/{wallet_id}')
    data = get_response.json()
    assert get_response.status_code == 200
    assert data.get('id') == wallet_id


@pytest.mark.asyncio
async def test_get_wallet_not_found(client: AsyncClient):
    """Тест для получения информации о несуществующем кошельке."""
    rand_uuid = uuid4()
    response = await client.get(f'/api/v1/wallets/{rand_uuid}')
    data = response.json()
    assert response.status_code == 404
    assert data.get('detail') == 'Wallet not found'
