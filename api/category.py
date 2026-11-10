from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_category
from schema import CategoryCreate, CategoryPublic, APIResponse

router = APIRouter()

# ---------------------------------------
# Create Category
# ---------------------------------------

@router.post("/create_category", status_code=status.HTTP_201_CREATED, response_model=APIResponse[CategoryPublic])
async def create_new_category(
    category_data: CategoryCreate, 
    session: AsyncSession = Depends(get_session)
):
    """
    Creates a new product category.
    """

    # Check whether a category with the same name already exists.
    category = await crud_category.fetch_category_by_name(category_data.name, session)

    if category:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Category with name '{category_data.name}' already exists!")

    new_category = await crud_category.create_category(category_data, session)
    return APIResponse(
        message = "New Category Created Sucessfully!", 
        data = new_category
    )

# -------------------------------------
# Fetch all Categories
# -------------------------------------

@router.get("/", response_model = APIResponse[list[CategoryPublic]])
async def fetch_all_categories(session: AsyncSession = Depends(get_session)):
    """
    Retrieves all available categories.
    Returns an empty list if no categories exist.
    """

    category_list = await crud_category.fetch_all_categories(session)

    return APIResponse(
        message = "Fetched all Categories", 
        data = category_list
    )

# -------------------------------------
# Fetch Category by ID
# -------------------------------------

@router.get("/id/{category_id}", response_model = APIResponse[CategoryPublic])
async def fetch_category_by_id(category_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieves category details using its primary key.
    """
    category = await crud_category.fetch_category_by_id(category_id, session)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found!")
    
    return APIResponse(
        message = "Fetched category data successfully!", 
        data = category
    ) 

# --------------------------------------
# Fetch Category by Name
# --------------------------------------

@router.get("/name/{category_name}", response_model = APIResponse[CategoryPublic])
async def fetch_category_by_name(category_name: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieves category details using its name.
    """

    category = await crud_category.fetch_category_by_name(category_name, session)

    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Category with name {category_name} not found!")

    return APIResponse(
        message = "Fetched category data successfully!",
        data = category
    )

# -------------------------------------
# TODO: Update a Category
# TODO: Delete a Category
# -------------------------------------