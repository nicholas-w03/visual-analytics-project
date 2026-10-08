from pathlib import Path

import cdsapi
import pandas as pd
from dotenv import load_dotenv

DATA = Path(__file__).resolve().parent.parent
load_dotenv(DATA.parent / ".env")      # loads CDSAPI_URL and CDSAPI_KEY before the client is created

OUT = DATA / "raw" / "era5"
OUT.mkdir(parents=True, exist_ok=True)

HALF = 0.15   # half-width of the box in degrees; keep equal to CHIRPS

regions = pd.read_csv(DATA / "reference" / "regions.csv")
client = cdsapi.Client()

for r in regions.itertuples():
    target = OUT / f"{r.country}_{r.region}.nc".replace(" ", "_")
    if target.exists():            # already fetched, skip
        continue
    client.retrieve(
        "reanalysis-era5-land-monthly-means",
        {
            "product_type": ["monthly_averaged_reanalysis"],
            "variable": ["2m_temperature"],
            "year": [str(y) for y in range(2010, 2024)],
            "month": [f"{m:02d}" for m in range(1, 13)],
            "time": ["00:00"],
            "area": [r.lat + HALF, r.lon - HALF, r.lat - HALF, r.lon + HALF],  # N, W, S, E
            "data_format": "netcdf",
            "download_format": "unarchived",
        },
    ).download(str(target))
    print("saved", target.name)