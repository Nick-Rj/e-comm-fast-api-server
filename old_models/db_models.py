from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user" # Explicitly define the table name
    
    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, index = True)
    hashed_password = Column(String)
    role = Column(String, default = "customer")

    # Mapping Review model with User model
    reviews = relationship("Review", back_populates = "user")

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key = True)
    text = Column(String)
    rating = Column(Integer)

    # Foreign key from User
    user_id = Column(Integer, ForeignKey("user.id"))

    # Mapping User model with Review model
    user = relationship("User", back_populates = "reviews")

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates = "reviews")