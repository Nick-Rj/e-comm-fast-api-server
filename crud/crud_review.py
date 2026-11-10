from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import Review
from schema import ReviewCreate

# ---------------------------------------
# Shared Review Query
# ---------------------------------------

def _review_query():
    """
    Base query for retrieving reviews with their related user.

    Eagerly loads Review.user because ReviewPublic includes UserPublic.
    This avoids implicit lazy-loading during async response serialization.
    """

    return select(Review).options(
        selectinload(Review.user)
    )

# --------------------------------------
# Create Review
# --------------------------------------

async def create_review(review_data: ReviewCreate, user_id: int, session: AsyncSession) -> Review:
    """
    Creates a new review for a product.
    Note: user_id must come from the authenticated user's identity.
    """

    # Convert the validated API schema into a dictionary.
    review_dict = review_data.model_dump()

    review_dict.pop("user_id", None)

    print(f"Review data in create: {review_data} {user_id}")
    # Create the database model.
    # user_id is supplied separately by the backend, not the client.
    db_review = Review(**review_dict, user_id = user_id)

    session.add(db_review)

    # Execute the INSERT and retrieve the generated review ID.
    # This transaction is not committed yet.
    await session.flush()

    # Reload the review with its associated user.
    statement = _review_query().where(Review.id == db_review.id)
    result = await session.exec(statement)

    created_review = result.one()

    # Commit the transaction to persist the review.
    await session.commit()
    
    return created_review

# -------------------------------------------
# Fetch Reviews By Product ID
# -------------------------------------------

async def get_reviews_by_product_id(product_id: int, session: AsyncSession) -> list[Review]:
    """
    Retrieves all reviews associated with a product.
    Returns an empty list if no reviews exist.
    """
    statement = _review_query().where(Review.product_id == product_id).order_by(Review.id)

    results = await session.exec(statement)
    return results.all()

# -------------------------------------------
# Fetch Reviews By User ID
# -------------------------------------------

async def get_reviews_by_user_id(user_id: int, session: AsyncSession) -> list[Review]:
    """
    Retrieves all reviews written by a specific user.
    Returns an empty list if no reviews exist.
    """
    statement = _review_query().where(Review.user_id == user_id).order_by(Review.id)

    results = await session.exec(statement)
    return results.all()

# TODO: [Update Review]
# TODO: [Delete Review] 