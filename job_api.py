import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
HEADERS = {
    "x-rapidapi-key": "RAPIDAPI_KEY",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
URL = "https://jsearch.p.rapidapi.com/search"

def fetch_jobs(query: str, location: str = "", num_pages: int = 1) -> List[Dict]:
    all_jobs = []
    for page in range(num_pages):
        params = {"query": query, "page": page + 1, "num_pages": num_pages}
        res = requests.get(URL, headers=HEADERS, params=params)
        data = res.json()
        jobs = data.get("data", [])
        if not jobs:
            break
        all_jobs.extend(jobs)
    return all_jobs