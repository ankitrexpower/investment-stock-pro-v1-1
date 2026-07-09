# Replace sample holdings with a real FII/DII data API when available.
# V1.1 rule: FII + DII >= 5%, Close > SMA121, CCI20 <= -192, D/W/M scan.

SAMPLE = [
    {"stock":"ABC LTD","fii":3.1,"dii":2.5,"D_Close":152,"D_SMA121":140,"D_CCI":-205,"W_Close":150,"W_SMA121":155,"W_CCI":-80,"M_Close":150,"M_SMA121":100,"M_CCI":-210},
    {"stock":"HAL","fii":4.4,"dii":2.7,"D_Close":3100,"D_SMA121":3000,"D_CCI":-198,"W_Close":3100,"W_SMA121":2800,"W_CCI":-215,"M_Close":3100,"M_SMA121":2500,"M_CCI":-90},
    {"stock":"XYZ LTD","fii":1.2,"dii":2.1,"D_Close":90,"D_SMA121":80,"D_CCI":-250,"W_Close":90,"W_SMA121":70,"W_CCI":-250,"M_Close":90,"M_SMA121":60,"M_CCI":-250},
    {"stock":"BEL","fii":2.8,"dii":3.0,"D_Close":280,"D_SMA121":300,"D_CCI":-210,"W_Close":280,"W_SMA121":250,"W_CCI":-199,"M_Close":280,"M_SMA121":200,"M_CCI":-205},
]

def get_holdings_and_price_data():
    return SAMPLE

def setup(row, tf):
    return row[f"{tf}_Close"] > row[f"{tf}_SMA121"] and row[f"{tf}_CCI"] <= -192

def scan_all():
    rows = get_holdings_and_price_data()
    qualified = [r for r in rows if (r["fii"] + r["dii"]) >= 5]
    results = {"D": [], "W": [], "M": []}
    for r in qualified:
        total = r["fii"] + r["dii"]
        for tf in ["D", "W", "M"]:
            if setup(r, tf):
                results[tf].append({"stock": r["stock"], "total_holding": total, "cci": r[f"{tf}_CCI"], "status":"SETUP"})
    return {"total_stocks": len(rows), "qualified_stocks": len(qualified), "total_setup": sum(len(v) for v in results.values()), "results": results}
