from fastapi import APIRouter

from app.routers.v1.wallets import router as wallets_router

router = APIRouter(prefix='/v1')
router.include_router(wallets_router)
