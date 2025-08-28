from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..models.student import Student


def create_student(student: Student, db: Session) -> Student:
    """ Create  a new  student  in the database.

    Args:
        student: Student object with name, age, email and grades.
        db: Database session.

    Returns:
        The created student object.

    Raises:
        HTTPException: if the email is already in use (duplicate).
        """
    db_student = Student(**student.model_dump())
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

def get_student(student_id: int, db: Session) -> Student:
    """
    Retrieve a student by ID.

    Args:
        student_id: ID of the student to retrieve.
        db: Database session.

    returns:
        The Student object if found.

    raises:
        HTTPException: if the student is not found.
    """

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def get_students(db: Session, skip: int = 0, limit: int = 10) -> List[Student]:
    """
    retrieve a list of students with pagination.

    Args:
        db: Database session.
        skip: Number of students to skip.
        limit: Maximum number of records to return.

    Returns:
        List of Student objects.
    """

    return db.query(Student).offset(skip).limit(limit).all()

def update_student(student_id: int, student_update: Student, db: Session) -> Student:
    """
    Update a student's information.

    Args:
        student_id: ID of the student to update.
        student_update: Student object with updated fields.
        db: Database session.

    Returns:
        The updated student object.

    Raises:
        HTTPException: if the student is not found or email is already in use.
    """
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

def delete_student(student_id: int, db: Session) -> None:
    """
    Delete a student by ID

    Args:
        student_id: ID of the student to delete.
        db: Database session.

    Raises:
        HTTPException: if the student is not found.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()