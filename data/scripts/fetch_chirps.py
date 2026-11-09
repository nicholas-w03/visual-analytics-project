import io
import time
from pathlib import Path

import pandas as pd
import requests
import sys

DATA = Path(__file__).resolve().parent.parent
OUT = DATA / "raw" / "chirps"
PROCESSED = DATA / "processed"
OUT.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

START, END = "2010-01-01", "2023-12-01"
BASE = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalMonthlyP05.csv"

regions = pd.read_csv(DATA / "reference" / "regions.csv")
points = regions.drop_duplicates("point_id")      # download once per unique location
failed = []

for r in points.itertuples():
    target = OUT / f"p{r.point_id:04d}.csv"
    if target.exists():            # already fetched, skip
        continue

    clat = round(round(r.lat / 0.1) * 0.1, 1)   # same snap as ERA5
    clon = round(round(r.lon / 0.1) * 0.1, 1)
    lat0, lat1 = round(clat - 0.125, 4), round(clat + 0.125, 4)   # 6x6 CHIRPS cells
    lon0, lon1 = round(clon - 0.125, 4), round(clon + 0.125, 4)
    url = (f"{BASE}?precip[({START}):1:({END})]"
           f"[({lat0}):1:({lat1})][({lon0}):1:({lon1})]")

    resp = None
    for attempt in range(1, 6):                        # up to 5 tries
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"{target.name} attempt {attempt} failed: {e}")
            resp = None
            time.sleep(15 * attempt)                   # back off: 15s, 30s, 45s...
    if resp is None:
        failed.append(target.name)
        continue
    
    df = pd.read_csv(io.StringIO(resp.text), skiprows=[1])        # row 2 is a units row
    assert df.groupby("time").size().eq(36).all(), target.name    # 6x6 cells per month
    df = df.groupby("time", as_index=False)["precip"].mean()      # average the cells in the box, per month
    df["point_id"] = r.point_id

    df.to_csv(target, index=False)
    print("saved", target.name)
    time.sleep(1)                  # be polite to a public server

if failed:
    print("FAILED, rerun the script to retry these:", failed)
    sys.exit(1)
    
m = pd.concat(pd.read_csv(p, parse_dates=["time"]) for p in sorted(OUT.glob("*.csv")))
m["year"] = m["time"].dt.year
yearly = (m.groupby(["point_id", "year"])
            .agg(rain_mm=("precip", "sum"), months=("precip", "count"))
            .reset_index())

# expand back to every region (shared locations get the same values)
yearly = (regions[["country", "region", "point_id"]]
          .merge(yearly, on="point_id")
          .sort_values(["country", "region", "year"]))
yearly.to_csv(PROCESSED / "chirps_region_year.csv", index=False)
print(yearly.head(15))