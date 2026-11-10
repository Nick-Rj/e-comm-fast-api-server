from passlib.context import CryptContext

# ---------------------------------------------
# PASSWORD HASHING CONFIGURATION
# ---------------------------------------------

# Centralized password hashing configuration.

# bcrypt is used for password hashing.
# deprecated = "auto" allows Passlib to identify outdated hashing schemas when additional schemas are introduced.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --------------------------------------------
# HASH PASSWORD
# --------------------------------------------

def hash_password(password: str) -> str:
    """
    Generated a secure hash of the supplied password.

    A new random salt is generated automatically.
    The original passowrd is never stored.
    """
    return pwd_context.hash(password)

# --------------------------------------------
# VERIFY PASSWORD
# --------------------------------------------

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against its stored hash.

    Returns True if the password matches; otherwise False.
    """
    return pwd_context.verify(password, hashed_password)