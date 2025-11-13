import pytest
from httpx import AsyncClient

from app.main import health, root


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Тест для главной страницы."""
    response = await client.get('/')
    data = response.json()
    assert response.status_code == 200
    assert data == await root()


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    """Тест для страницы проверки состояния сервиса."""
    response = await client.get('/health')
    data = response.json()
    assert response.status_code == 200
    assert data == await health()
