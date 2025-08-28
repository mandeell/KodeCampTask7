from fastapi import FastAPI
from .utils import create_db_and_tables, configure_cors, configure_logging_middleware
from .routers import student_router, auth_router

app = FastAPI(
    title="Student Management System",
    description="A FastAPI backend for managing students and their grades",
    version="1.0.0"
)

configure_cors(app)
configure_logging_middleware(app)

# Include routers
app.include_router(student_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Student Management System API"}