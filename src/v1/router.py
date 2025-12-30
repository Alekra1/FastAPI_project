from fastapi import APIRouter

from .book.routers import router as book_routers
from .item.routers import router as item_routers

router = APIRouter(prefix="/api/v1")

router.include_router(item_routers)
router.include_router(book_routers)
