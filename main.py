from fastapi import FastAPI
from api import user, product, category, review

app = FastAPI(
    title = "E-commerce App",
    description = "Product Catalog and Inventory Management API",
    version = "1.0.0"
)

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(product.router, prefix='/api/v1/products', tags=["Products"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Reviews"])

@app.get('/', tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm that the API is running.
    """
    return {'message':"Welcome to the E-commerce API!"}