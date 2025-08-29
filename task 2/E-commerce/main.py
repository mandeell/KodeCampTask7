from fastapi import FastAPI
from .utils import create_db_and_tables, configure_cors, response_time_setup
from .routers import cart_router, users_router, admin_product_router, public_product_router

app = FastAPI()

configure_cors(app)
response_time_setup(app)

app.include_router(users_router)
app.include_router(cart_router)
app.include_router(admin_product_router)
app.include_router(public_product_router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_db_and_tables()

