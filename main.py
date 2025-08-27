# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
import bcrypt

from adapters.mock import MockAdapter
from adapters.gemini import GeminiAdapter
from adapters.fal_adapter import FalAdapter

load_dotenv()

app = FastAPI(title="VideoNation AI")

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/mockvideos", StaticFiles(directory="mockvideos"), name="mockvideos")


# Templates folder (HTML files)
templates = Jinja2Templates(directory="templates")

JOB_STORE = {}

class GenerateRequest(BaseModel):
    prompt: str
    style: Optional[str] = None
    aspect: Optional[str] = None


def _combine_prompt(prompt: str, style: Optional[str], aspect: Optional[str]) -> str:
    pieces = [prompt.strip()]
    if style:
        pieces.append(f"Style: {style}")
    if aspect:
        pieces.append(f"Aspect: {aspect}")
    return "\n".join(pieces)


# --- MongoDB connection ---
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
users = db["users"]


# --- Auth APIs ---
@app.post("/api/signup")
async def api_signup(
    name: str = Form(...), email: str = Form(...), password: str = Form(...)
):
    if users.find_one({"email": email}):
        return JSONResponse({"error": "User already exists"}, status_code=400)

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.insert_one({"name": name, "email": email, "password": hashed_pw})
    return {"message": "Signup successful. Please login."}


@app.post("/api/login")
async def api_login(email: str = Form(...), password: str = Form(...)):
    user = users.find_one({"email": email})
    if not user:
        return JSONResponse({"error": "Invalid credentials"}, status_code=400)

    if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return {"message": "Login successful"}
    return JSONResponse({"error": "Invalid credentials"}, status_code=400)


# --- Video Generation APIs ---
@app.post("/generate")
async def generate(req: GenerateRequest):
    combined = _combine_prompt(req.prompt, req.style, req.aspect)
    adapter = FalAdapter()
    try:
        result = await adapter.generate(combined, req.aspect)
        msg = "Video successfully generated."
    except Exception as e:
        mock = MockAdapter()
        result = await mock.generate(combined)
        msg = f"API unavailable or failed ({str(e)}). Showing mock video."

    return {
        "video_url": result["video_url"],
        "message": msg,
        "job_id": result.get("job_id"),
    }


@app.post("/refine")
async def refine(req: GenerateRequest):
    adapter = GeminiAdapter()
    combined = _combine_prompt(req.prompt, req.style, req.aspect)
    try:
        refined_prompt = await adapter.refine_prompt(combined)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refine failed: {str(e)}")
    return {"original_prompt": req.prompt, "refined_prompt": refined_prompt}


@app.get("/status/{job_id}")
async def status(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# --- HTML Pages ---
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/video")
async def video_page(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
