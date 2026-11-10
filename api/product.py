# Using the methods created for CRUD operations in the API calls

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

# Importing get_session for creating db sessions for the API calls
from core.db import get_session

# Importing methods for CRUD operations
from crud import crud_product

# Importing schemas for API calls
from schema import ProductCreate, ProductPublic, APIResponse

# This APIRouter will create the path for these API endpoints, Product endpoints.
# Instead of calling each Product endpoint in the main.py, only this router will be called with a proper prefix.
router = APIRouter()

# Creating endpoints for the Product

@router.post(
    "/create_product",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[ProductPublic]
)
async def create_new_product(
    product_data: ProductCreate,
    # Dependency Injection for injecting the session created from session factory.
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new product.
    """
    new_product = await crud_product.create_product(product_data, session)

    return APIResponse(
        message = "New Product Created Successfully!",
        data = new_product
    )

@router.get(
    "/",
    response_model=APIResponse[list[ProductPublic]]
)
async def fetch_all_products(
    session: AsyncSession = Depends(get_session)
):
    """
    Get a list of all products.
    """
    all_products = await crud_product.fetch_all_products(session)

    return APIResponse(
        message = "All products fetched!", 
        data = all_products
    )

@router.get(
    "/{product_id}",
    response_model=APIResponse[ProductPublic]
)
async def fetch_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get details for a specific product by ID.
    """
    product = await crud_product.fetch_product_by_id(product_id, session)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not available")
    
    return APIResponse(
        message = "Product details fetched successfully!", 
        data = product
    )

# TODO: Update Product
# TODO: Fetch Products by Category
# TODO: Delete a Product