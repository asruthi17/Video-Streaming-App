from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from passlib.hash import bcrypt
import sqlite3
import os

app = FastAPI()

# Allow CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create video folder if it doesn't exist
VIDEO_FOLDER = "videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# DB setup
DB_NAME = "streaming.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize tables
with get_db() as conn:
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            filename TEXT
        )
    ''')
    conn.commit()

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class Video(BaseModel):
    id: int
    title: str
    category: str
    filename: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register user
@app.post("/register")
def register(user: User):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (user.username,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pwd = bcrypt.hash(user.password)
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_pwd))
    conn.commit()
    return {"message": "User registered successfully"}

# User login
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (form_data.username,))
    user = cur.fetchone()
    if not user or not bcrypt.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user["username"], "token_type": "bearer"}

# Get all videos or by category
@app.get("/videos", response_model=List[Video])
def get_videos(category: Optional[str] = None):
    conn = get_db()
    cur = conn.cursor()
    if category:
        cur.execute("SELECT * FROM videos WHERE category=?", (category,))
    else:
        cur.execute("SELECT * FROM videos")
    rows = cur.fetchall()
    return [Video(id=row["id"], title=row["title"], category=row["category"], filename=row["filename"]) for row in rows]

# Get available video categories
@app.get("/categories", response_model=List[str])
def list_categories():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM videos")
    rows = cur.fetchall()
    return [row["category"] for row in rows if row["category"]]

@app.get("/")
def read_home():
    return {
        "message": "Welcome to the Video Streaming App!",
        "visit_docs": "Go to /docs to view the API documentation.",
        "endpoints": ["/register", "/token", "/videos", "/categories", "/stream/{filename}"]
    }

# Stream video
@app.get("/stream/{filename}")
def stream_video(filename: str):
    path = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path, media_type="video/mp4")
