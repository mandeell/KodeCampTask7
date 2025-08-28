from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..utils import get_session
from ..crud.student import (
    create_student,
    get_student, 
    get_students,
    update_student,
    delete_student
)
from ..schemas import StudentCreate, StudentUpdate, StudentResponse
from ..models import Student, User

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student_endpoint(
        student: StudentCreate,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Create a new student"""
    # Convert Pydantic model to SQLModel
    db_student = Student(**student.model_dump())
    return create_student(db_student, db)

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_endpoint(student_id: int, db: Session = Depends(get_session)):
    """Get a student by ID"""
    return get_student(student_id, db)

@router.get("/", response_model=List[StudentResponse])
async def get_students_endpoint(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_session)
):
    """Get all students with pagination"""
    return get_students(db, skip=skip, limit=limit)

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_endpoint(
    student_id: int, 
    student_update: StudentUpdate, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a student"""
    # Convert Pydantic model to SQLModel, excluding unset fields
    db_student = Student(**student_update.model_dump(exclude_unset=True))
    return update_student(student_id, db_student, db)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_endpoint(
        student_id: int,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """Delete a student"""
    delete_student(student_id, db)
    return None

