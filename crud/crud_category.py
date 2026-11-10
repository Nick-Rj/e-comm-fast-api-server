from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.models import Category
from schema import CategoryCreate

# --------------------------------------------
# Create Category
# --------------------------------------------

async def create_category(category_data: CategoryCreate, session: AsyncSession) -> Category:
    """
    Creates a new category.
    """

    # Convert the validated API schema into a database model.
    db_category = Category.model_validate(category_data)

    # Add the category to the current database session.
    session.add(db_category)

    # Commit the transaction to persist the category.
    await session.commit()

    # Refresh the object with the latest database values.
    await session.refresh(db_category)

    return db_category

# --------------------------------------------
# Fetch All Categories
# --------------------------------------------

async def fetch_all_categories(session: AsyncSession) -> list[Category]:
    """
    Retrieves all categories.
    Returns an empty list if no categories exist.
    """

    statement = select(Category).order_by(Category.id)
    results = await session.exec(statement)

    return results.all()

# -------------------------------------------
# Fetch Category By ID
# -------------------------------------------

async def fetch_category_by_id(category_id: int, session: AsyncSession) -> Category | None:
    """
    Retrieves a category by its primary key.
    Returns None if the category does not exist.
    """

    statement = select(Category).where(Category.id == category_id)
    result = await session.exec(statement)

    return result.one_or_none()

async def fetch_category_by_name(category_name: str, session: AsyncSession) -> Category | None:
    """
    Retrieves a category by its username.
    Returns None if the category does not exist
    """

    statement = select(Category).where(Category.name == category_name)
    result = await session.exec(statement)

    return result.one_or_none()

