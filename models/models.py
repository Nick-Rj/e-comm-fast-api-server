from sqlmodel import Field, Relationship, SQLModel

# Creating all the models for the FastAPI app

# --------------------------------------------------
# CATEGORY MODEL
# --------------------------------------------------

# If table != True, it will not create table in the DB, as this class will not represent a database table.
# Field() defines database columns and their properties. It allows to configure additional properties of a model attribute.
# Relationship() defines ORM-level relationships between model objects.

class Category(SQLModel, table = True):
    # Primary Key, The database generates the ID when a new category is inserted.
    id: int | None = Field(default = None, primary_key = True)

    # Category name must be unique.
    # index: requests a database index
    name: str = Field(index = True, unique = True)

    # Mapping Product model with Category model.
    # One Category can have multiple Products.
    # back_populates connects this relationship to Product.category.
    product: list["Product"] = Relationship(back_populates = "category")

# -------------------------------------------------
# USER MODEL
# -------------------------------------------------

class User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)

    # Username must be unique across all users.
    username: str = Field(index = True, unique = True)

    # Real User Registration should have securely hashed password storage.
    # The API endpoint is responsible for hashing before persistence.
    password: str

    # Application-side default role for newly created users.
    role: str = "customer"

    # Mapping Review model with User model for user reviews.
    # One User can write multiple Reviews.
    reviews: list["Review"] = Relationship(back_populates = "user")

# --------------------------------------------------
# PRODUCT MODEL
# --------------------------------------------------

class Product(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    name: str = Field(index = True)
    description: str
    price: float

    # Foreign key referencing Category.id
    # Every Product must belong to a Category.
    # Index helps queries that filter products by category.
    category_id: int = Field(foreign_key = "category.id", index = True)

    # ORM relationship with Category.
    category: Category = Relationship(back_populates = "product")

    # Mapping Review model with Product model.
    # One Product can have multiple Reviews.
    reviews: list["Review"] = Relationship(back_populates = "product")

# -------------------------------------------------
# REVIEW MODEL:
# -------------------------------------------------

class Review(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    text: str
    rating: float

    # Foreign key referencing User.id.
    # Index helps queries that fetch reviews by user.
    user_id: int = Field(foreign_key = "user.id", index = True)

    # Mapping User model with Review model
    # Each Review belongs to one User.
    user: User = Relationship(back_populates = "reviews")

    # Foreign key referencing Product.id
    # Index helps queries that fetch reviews by product.
    product_id: int = Field(foreign_key = "product.id", index = True)

    # Each Review belongs to one Product
    product: Product = Relationship(back_populates = "reviews")