from .student import router as student_router
from .auth import router as auth_router

__all__ = [
    "student_router",
    "auth_router"
]
