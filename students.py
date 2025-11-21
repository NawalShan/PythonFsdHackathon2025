from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from typing import List,Optional
import sqlite3


app = FastAPI()

# DB
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            score REAL NOT NULL   
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------------
# Pydantic models
# ----------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str
    score: float
class StudentCreate(BaseModel):
    name: str
    age: int
    Course: str
    Score: float
class StudentUpdate(BaseModel):
    name: str = None
    age: int = None
    Course: str = None
    Score: float = None
 

# ----------------------------
# CRUD Endpoints
# ----------------------------
@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, course, score) VALUES (?, ?, ?, ?)",
        (student.name, student.age, student.course, student.score)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return Student(id=student_id, **student.dict())


@app.get("/students/", response_model=List[Student])
def read_students():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return [Student(**dict(row)) for row in rows]


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**dict(row))


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    updated_fields = student.dict(exclude_unset=True)

    for key, value in updated_fields.items():
        conn.execute(f"UPDATE students SET {key} = ? WHERE id = ?", (value, student_id))

    conn.commit()

    updated_row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return Student(**dict(updated_row))


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")

    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return {"detail": "Student deleted successfully....."}
   


    


