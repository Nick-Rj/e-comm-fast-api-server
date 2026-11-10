# Developing SQL queries as Python objects.

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import Product, Review
from schema import ProductCreate

# ---------------------------------------------
# Shared Product Query
# ---------------------------------------------

def _product_query():
    """
    Base query for retrieving products with their related data.

    Eagerly loads relationships required by ProductPublic:
    - Product category
    - Product reviews
    - User associated with each review

    This avoids implicit lazy-loading during async response serialization.
    """
    return select(Product).options(
        selectinload(Product.category),
        selectinload(Product.reviews).selectinload(Review.user)
    )

# ---------------------------------------------
# Create Product
# ---------------------------------------------

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    """
    Creates a new product and returns it with related data.
    """
    
    # Convert the validated API schema into a database model.
    db_product = Product.model_validate(product_data)
    
    # Add the product to the current database session.
    session.add(db_product)

    # Execute pending SQL statements, including the INSERT.
    # The generated primary key becomes available after flushing.
    # The transcation is not committed yet.
    await session.flush()

    # Retrive the newly created product along with its relationships.
    statement = _product_query().where(Product.id == db_product.id)
    result = await session.exec(statement)

    created_product = result.one()

    # Commit the transaction to persist the product.
    await session.commit()
    
    return created_product

# ---------------------------------------------
# Fetch All Products
# ---------------------------------------------

async def fetch_all_products(session: AsyncSession) -> list[Product]:
    """
    Retrieves all products with their related data.
    Returns an empty list if no products exists.
    """
    
    statement = _product_query().order_by(Product.id)
    results = await session.exec(statement)
    return results.all()

# ---------------------------------------------
# Fetch Product by ID
# ---------------------------------------------

async def fetch_product_by_id(product_id: int, session: AsyncSession) -> Product | None:
    """
    Retrieves a product by its primary key.
    Returns None if the product does not exist.
    """
    
    statement = _product_query().where(Product.id == product_id)
    result = await session.exec(statement)
    return result.one_or_none()
