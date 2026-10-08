import io
import time
from pathlib import Path

import pandas as pd
import requests

DATA = Path(__file__).resolve().parent.parent
OUT = DATA / "raw" / "chirps"
PROCESSED = DATA / "processed"
OUT.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

START, END = "2010-01-01", "2023-12-01"
HALF = 0.15   # half-width of the box in degrees; keep equal to ERA5
BASE = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalMonthlyP05.csv"

regions = pd.read_csv(DATA / "reference" / "regions.csv")

for r in regions.itertuples():
    target = OUT / f"{r.country}_{r.region}.csv".replace(" ", "_")
    if target.exists():            # already fetched, skip
        continue

    lat0, lat1 = round(r.lat - HALF, 4), round(r.lat + HALF, 4)
    lon0, lon1 = round(r.lon - HALF, 4), round(r.lon + HALF, 4)
    url = (f"{BASE}?precip[({START}):1:({END})]"
           f"[({lat0}):1:({lat1})][({lon0}):1:({lon1})]")

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text), skiprows=[1])        # row 2 is a units row
    df = df.groupby("time", as_index=False)["precip"].mean()      # average the cells in the box, per month
    df["region"], df["country"] = r.region, r.country

    df.to_csv(target, index=False)
    print("saved", target.name)
    time.sleep(1)                  # be polite to a public server

m = pd.concat(pd.read_csv(p, parse_dates=["time"]) for p in sorted(OUT.glob("*.csv")))
m["year"] = m["time"].dt.year
yearly = (m.groupby(["country", "region", "year"])
            .agg(rain_mm=("precip", "sum"), months=("precip", "count"))
            .reset_index())
yearly.to_csv(PROCESSED / "chirps_region_year.csv", index=False)
print(yearly.head(15))