from fastapi import APIRouter

from .products.router import router as products_router

router = APIRouter(prefix="/api/v1")

router.include_router(router=products_router, prefix="/products", tags=["Products"])
