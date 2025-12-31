from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .database import create_db_and_tables
from .routers import auth, files, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Ensure static directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static/plots", exist_ok=True)
    yield

app = FastAPI(
    lifespan=lifespan, 
    title="DataChat AI Analytics API",
    description="🚀 AI-Powered Data Analytics Platform - Built by Atta Ur Rehman (@Iatta56)",
    version="2.0.0",
    contact={
        "name": "Atta Ur Rehman",
        "url": "https://github.com/Iatta56",
    },
)

# Configure CORS for Frontend
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to DataChat AI Analytics API",
        "version": "2.0.0",
        "author": "Atta Ur Rehman",
        "github": "https://github.com/Iatta56",
        "features": [
            "🤖 AI-Powered Data Analysis",
            "📊 Smart Visualizations",
            "📈 Trend Prediction",
            "🔍 Natural Language Queries",
            "📁 Multi-Format File Support",
            "🔐 Secure Authentication"
        ]
    }
