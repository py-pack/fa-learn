from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud, repositories
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .repositories import product_by_id

router = APIRouter()


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await repositories.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_products(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    product_in: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_in,
    )


@router.patch("/{product_id}/", response_model=Product)
async def update_product_partial(
    product_in: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.update_product(
        session=session, product=product, product_update=product_in, partial=True
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
