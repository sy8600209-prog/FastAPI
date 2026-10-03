from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# database aur table banao (ek baar)
def init_db():
    conn = sqlite3.connect("mydata.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

class User(BaseModel):
    name: str
    age: int

# data daalna (INSERT)
@app.post("/users")
def add_user(user: User):
    conn = sqlite3.connect("mydata.db")
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (user.name, user.age))
    conn.commit()
    conn.close()
    return {"message": "user add ho gaya"}

# saara data dekhna (SELECT)
@app.get("/users")
def get_users():
    conn = sqlite3.connect("mydata.db")
    rows = conn.execute("SELECT id, name, age FROM users").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "age": r[2]} for r in rows]