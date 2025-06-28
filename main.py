from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

@app.post("/find-jobs/")
async def find_jobs(request: Request):
    try:
        body = await request.json()
        skills = body.get("skills", "")
        location = body.get("location", "")
        page = int(body.get("page", 1))

        url = f"https://{RAPIDAPI_HOST}/search"
        querystring = {
            "query": skills,
            "page": str(page),
            "num_pages": "1",
            "location": location,
        }

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }

        response = requests.get(url, headers=headers, params=querystring, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {"jobs": data.get("data", [])}
        else:
            return {"error": f"Failed to fetch jobs. Code {response.status_code}", "details": response.text}

    except Exception as e:
        return {"error": str(e)}
