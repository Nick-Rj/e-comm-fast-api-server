from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Generic, TypeVar

# As table=True is not added, these models are used for API input/output validation and are distinct from the database models.
# This allows us to control what data is exposed via the API for CRUD operations.

# --------------------------------------------------
# Category Schemas
# --------------------------------------------------

# Shared properties for a category.
class CategoryBase(SQLModel):
    name: str

# Properties required when creating a new category (API input).
class CategoryCreate(CategoryBase):
    pass

# Properties returned by the API (API output).
class CategoryPublic(CategoryBase):
    id: int

    # Optional: Include products belonging to this category.
    # Kept disabled to avoid deeply nested/circular response structure.
    # products: list[ProductPublic] = Field(default_factory = list)

# --------------------------------------------------
# User Schemas
# --------------------------------------------------

# Shared properties for a user.
class UserBase(SQLModel):
    username: str
    # role: str = "customer"

# Properties for creating a new user (API input).
class UserCreate(UserBase):
    # Plain-text password received from the client.
    # The endpoint will hash it before storing it in the database.
    password: str

# Properties for updating a user's role (API input).
class UserRoleUpdate(UserBase):
    role: str

    # Username is used to identify and validate the target user.
    # Role is the new role to be assigned.
    # This endpoint must be restricted to authorized administrators.

# Properties returned by the API (API output).
class UserPublic(UserBase):
    id: int
    role: str

    # Never expose the password or password hash in API responses.
    # Optional: Include reviews written by the user.
    # reviews: list[ReviewPublic] = Field(default_factory = list)

# ---------------------------------------------------
# Review Schemas
# ---------------------------------------------------

# Shared properties for a review.
class ReviewBase(SQLModel):
    text: str
    rating: float

# Properties for creating a new review (API input).
class ReviewCreate(ReviewBase):
    # user_id: int [excluded] 
    # It will be obtained from the currently authenticated user later.
    product_id: int

# Properties returned by the API (API output).
class ReviewPublic(ReviewBase):
    id: int

    # Nested schema: Includes public details of the review's author.
    user: UserPublic

    # Optional: Includes product details in the review response.
    # Kept disabled to avoid circular nested response structures.
    # product: ProductPublic

# Properties for updating an existing review (API input)
class ReviewUpdate(SQLModel):
    # Optional fields allow partial updates (PATCH).
    text: str | None
    rating: float | None

    # user_id is excluded; reviews belong to their original author.
    # product_id is excluded; a review should remain associated with its originally selected product.
    
    # Use model_dump(exclude_unset = True) when applying updates
    # so only fields supplied by the client are updated.


# ------------------------------------------------
# Product Schemas
# ------------------------------------------------

# Shared properties for a product.
class ProductBase(SQLModel):
    name: str
    description: str
    price: float

# Properties for creating a new product (API input).
class ProductCreate(ProductBase):
    # Foreign key: The product must belong to an existing category.
    category_id: int

# Properties returned by the API (API output).
class ProductPublic(ProductBase):
    id: int

    # Nested schema: Includes category details instead of only category_id.
    category: CategoryPublic

    # Nested schema: Includes reviews associated with this product.
    # default_factory creates a separate empty list for each instance.
    reviews: list[ReviewPublic] = Field(default_factory = list)


T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    message: str
    data: T