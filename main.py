from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from data_provider import scan_all

app = FastAPI(title="INVESTMENT STOCK PRO V1.1 API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"app":"INVESTMENT STOCK PRO V1.1", "status":"running"}

@app.get("/scan")
def scan():
    result = scan_all()
    result["last_scan"] = datetime.now().strftime("%I:%M %p")
    return result
