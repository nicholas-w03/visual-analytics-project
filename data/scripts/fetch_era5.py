from pathlib import Path

import cdsapi
import pandas as pd
from dotenv import load_dotenv

DATA = Path(__file__).resolve().parent.parent
load_dotenv(DATA.parent / ".env")      # loads CDSAPI_URL and CDSAPI_KEY before the client is created

OUT = DATA / "raw" / "era5"
OUT.mkdir(parents=True, exist_ok=True)

regions = pd.read_csv(DATA / "reference" / "regions.csv")
points = regions.drop_duplicates("point_id")      # download once per unique location
client = cdsapi.Client()

for r in points.itertuples():
    target = OUT / f"p{r.point_id:04d}.nc"
    if target.exists():            # already fetched, skip
        continue

    clat = round(round(r.lat / 0.1) * 0.1, 1)   # snap to ERA5-Land cell centre
    clon = round(round(r.lon / 0.1) * 0.1, 1)

    client.retrieve(
        "reanalysis-era5-land-monthly-means",
        {
            "product_type": ["monthly_averaged_reanalysis"],
            "variable": ["2m_temperature"],
            "year": [str(y) for y in range(2010, 2024)],
            "month": [f"{m:02d}" for m in range(1, 13)],
            "time": ["00:00"],
            "area": [clat + 0.1, clon - 0.1, clat - 0.1, clon + 0.1],  # N, W, S, E: 3x3 cells
            "data_format": "netcdf",
            "download_format": "unarchived",
        },
    ).download(str(target))
    print("saved", target.name)