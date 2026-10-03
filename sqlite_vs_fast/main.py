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







# for supabase key type system

# from fastapi import Header, HTTPException

# API_KEY = "meri-secret-key"

# @app.get("/users")
# def get_users(x_api_key: str = Header(...)):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Galat key")
#     ...





#-----------------------------------------------------------------------
# steamlit se ConnectionAbortedError
# import streamlit as st
# import requests

# res = requests.get("http://127.0.0.1:8000/users")
# st.table(res.json())