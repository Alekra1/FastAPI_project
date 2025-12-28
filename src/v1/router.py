from fastapi import APIRouter

from .item.routers import router as item_routers

router = APIRouter(prefix="/api/v1")

router.include_router(item_routers)
