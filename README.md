# INVESTMENT STOCK PRO V1.1 Hosting Ready

V1.1 rules:
- FII + DII >= 5%
- Daily / Weekly / Monthly scan
- Close > SMA121
- CCI(20) <= -192
- SETUP only

## Frontend hosting
Upload `frontend` folder to Netlify / Cloudflare Pages.

## Backend hosting
Upload `backend` folder to Render.
Run command:
`pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT`

## Important
`backend/data_provider.py` currently has sample provider + price logic skeleton. For real automatic FII/DII data, connect a paid/free data API in `get_holdings()`.
