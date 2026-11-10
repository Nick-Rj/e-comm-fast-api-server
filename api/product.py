# Using the methods created for CRUD operations in the API calls

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

# Importing get_session for creating db sessions for the API calls
from core.db import get_session

# Importing methods for CRUD operations
from crud import crud_product, crud_category

# Importing schemas for API calls
from schema import ProductCreate, ProductPublic, APIResponse

# This APIRouter will create the path for these API endpoints, Product endpoints.
# Instead of calling each Product endpoint in the main.py, only this router will be called with a proper prefix.
router = APIRouter()

# -----------------------------------------
# Create Product
# -----------------------------------------

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
    Creates a new product associated with an existing category.
    """
    
    # Verify that the supplied category exists.
    category = await crud_category.fetch_category_by_id(product_data.category_id, session)

    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Category with ID '{product_data.category_id}' not found!")

    new_product = await crud_product.create_product(product_data, session)

    return APIResponse(
        message = "New Product Created Successfully!",
        data = new_product
    )

# ------------------------------------
# Fetch All Products
# ------------------------------------

@router.get(
    "/",
    response_model=APIResponse[list[ProductPublic]]
)
async def fetch_all_products(
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieves all products with their related category and reviews.
    """
    all_products = await crud_product.fetch_all_products(session)

    return APIResponse(
        message = "All products fetched successfully!", 
        data = all_products
    )

# -----------------------------------------
# Fetch Product by ID
# -----------------------------------------

@router.get(
    "/{product_id}",
    response_model=APIResponse[ProductPublic]
)
async def fetch_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieves product details using the product ID.
    """

    product = await crud_product.fetch_product_by_id(product_id, session)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not found!")
    
    return APIResponse(
        message = "Product details fetched successfully!", 
        data = product
    )

# ---------------------------------------
# TODO: Update Product
# TODO: Fetch Products by Category
# TODO: Delete a Product
# ---------------------------------------