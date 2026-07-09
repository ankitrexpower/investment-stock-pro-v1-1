from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
from io import StringIO
from data_provider import run_scan, sample_holdings

app = FastAPI(title="INVESTMENT STOCK PRO V2.0 REAL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"app": "INVESTMENT STOCK PRO V2.0 REAL", "status": "running", "rules": "FII+DII>=5, D/W/M, Close>SMA121, CCI<=-192"}

@app.get("/sample-scan")
def sample_scan():
    df = sample_holdings()
    return run_scan(df)

@app.post("/scan-csv")
async def scan_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    df = pd.read_csv(StringIO(text))
    return run_scan(df)

@app.get("/app", response_class=HTMLResponse)
def app_page():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
