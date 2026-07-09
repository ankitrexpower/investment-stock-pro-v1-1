# INVESTMENT STOCK PRO V2.0 REAL

Rules:
- FII + DII >= 5%
- Daily/Weekly/Monthly scan
- Close > SMA121
- CCI(20) <= -192
- SETUP only

Render commands:
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT

Open UI:
https://YOUR-RENDER-URL.onrender.com/app

Note: FII/DII holding input is CSV/API-ready. Price history uses yfinance.
