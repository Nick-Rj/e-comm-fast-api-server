from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.models import User
from schema import UserCreate, UserRoleUpdate

# ---------------------------------------
# Create User
# ---------------------------------------

async def create_user(user_data: UserCreate, hashed_password: str, session: AsyncSession) -> User:
    """
    Creates a new user with a securely hashed password.

    The endpoint is responsible for hashing the raw password before passing it to this CRUD function.
    """

    # Exclude the plain-text password received from the API request.
    user_dict = user_data.model_dump(exclude=["password"])

    # Create the database model using the hashed password.
    # The default role defined in the User model is applied automatically.
    db_user = User(**user_dict, password=hashed_password)

    session.add(db_user)
    await session.commit()

    # Reload database-generated values after insertion, including the generated ID.
    await session.refresh(db_user)

    return db_user

# -------------------------------------
# Fetch User by ID
# -------------------------------------    

async def fetch_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    """
    Retrieves a user by their primary key.
    Returns None if the user doesn't exists.
    """
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)

    return result.one_or_none()

# ------------------------------------
# Fetch User by Username
# ------------------------------------

async def fetch_user_by_username(username: str, session: AsyncSession) -> User | None:
    """
    Retrieves a user by their username.
    Returns None if the user doesn't exists.
    """
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)

    return result.one_or_none()

# --------------------------------------
# Update User Role
# --------------------------------------

async def update_user_role(user_data: UserRoleUpdate, session: AsyncSession) -> User | None:
    """
    Updates the role of an existing user.
    Identifies the user using their username.
    Returns None if the user doesn't exists.
    """
    statement = select(User).where(User.username == user_data.username)
    result = await session.exec(statement)

    db_user = result.one_or_none()

    if db_user is None:
        return None

    # Update the existing ORM object.
    # SQLAlchemy automatically tracks the modification.
    # No need to create a new User instance or call session.add().
    db_user.role = user_data.role

    await session.commit()

    # Refresh the object with the latest database values.
    await session.refresh(db_user)

    return db_user

