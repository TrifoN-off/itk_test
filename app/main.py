from fastapi import FastAPI

from app.routers.v1 import router as v1_router
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(v1_router, prefix='/api')


@app.get('/')
async def root():
    """Главная страница."""
    return {
        'message': 'Wallet API',
        'docs': '/docs',
        'health_check': '/health'
    }


@app.get('/health')
async def health():
    """Health check."""
    return {'status': 'OK'}
