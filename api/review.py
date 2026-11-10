from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_review, crud_product
from schema import ReviewCreate, ReviewPublic, APIResponse

router = APIRouter()

# -------------------------------------------
# Schema for Review with User ID
# -------------------------------------------

# user_id must be extracted from a JWT token after the user logs in.
class ReviewCreateWithUser(ReviewCreate):
    user_id: int

# -------------------------------------------
# Create Review
# -------------------------------------------

@router.post("/create_review", status_code = status.HTTP_201_CREATED, response_model = APIResponse[ReviewPublic])
async def create_new_review(
    review_data: ReviewCreateWithUser, 
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new review for a product.
    """
    # Check if the product exists.
    product = await crud_product.fetch_product_by_id(review_data.product_id, session)

    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Product with ID {review_data.product_id} not found!"
        )
    created_review = await crud_review.create_review(
        review_data, 
        user_id= review_data.user_id,
        session = session
    )

    return APIResponse(
        message = "New Review added Sucessfully!", 
        data = created_review
    )

# -----------------------------------------
# Fetch Reviews by Product ID
# -----------------------------------------

@router.get("/reviews/{product_id}", response_model = APIResponse[list[ReviewPublic]])
async def get_reviews_by_product_id(
    product_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieves all reviews associated with a product.
    Returns an empty list if no reviews exist.
    """

    reviews = await crud_review.get_reviews_by_product_id(product_id, session)

    return APIResponse(
        message = "Reviews fetched sucessfully!", 
        data = reviews
    )

# --------------------------------
# TODO: Update Review
# TODO: Delete Review
# --------------------------------
