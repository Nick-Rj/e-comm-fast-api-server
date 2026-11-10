from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creating method for hashing password before storing it in DB.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Creating method for verifying user's password
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)