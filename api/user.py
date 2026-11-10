from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_user
from schema import UserCreate, UserPublic, APIResponse
from core.security import verify_password, hash_password

router = APIRouter()

# ---------------------------------------------
# Create User
# ---------------------------------------------

@router.post(
    "/create_user", 
    status_code = status.HTTP_201_CREATED, 
    response_model=APIResponse[UserPublic]
)
async def create_new_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Creates a new user account.

    Checks username availability, hashes the password, and persists the user in the database.
    """

    # Checks whether the username is already registered.
    user = await crud_user.fetch_user_by_username(user_data.username, session)

    if user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail="User with same username already exists!"
        )

    hashed_password = hash_password(user_data.password)

    created_user = await crud_user.create_user(user_data, hashed_password, session)

    return APIResponse(
        message= "User signed up sucessfully!", 
        data= created_user
        )

# -------------------------------------
# Fetch User by ID
# -------------------------------------

@router.get("/id/{user_id}", response_model = APIResponse[UserPublic])
async def get_user_by_id(
    user_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """
    Fetches user details using the user's primary key, i.e., user_id.
    """
    user_data = await crud_user.fetch_user_by_id(user_id, session)

    if not user_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail=f"User with user ID {user_id} not found!"
        )

    return APIResponse(
        message = "User data fetched sucessfully!", 
        data = user_data
    )

# -------------------------------------
# Fetch User by Username
# -------------------------------------

@router.get("/username/{username}", response_model = APIResponse[UserPublic])
async def get_user_by_username(
    username: str, 
    session: AsyncSession = Depends(get_session)
):
    """
    Fetches user details using their username.
    """
    
    user_data = await crud_user.fetch_user_by_username(username, session)

    if not user_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with username {username} not found!"
        )

    return APIResponse(
        message = "User data fetched sucessfully!", 
        data = user_data
    )
