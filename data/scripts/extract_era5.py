from pathlib import Path

import pandas as pd
import xarray as xr

DATA = Path(__file__).resolve().parent.parent
PROCESSED = DATA / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

regions = pd.read_csv(DATA / "reference" / "regions.csv")

out, first = [], True
for r in regions.itertuples():
    f = DATA / "raw" / "era5" / f"{r.country}_{r.region}.nc".replace(" ", "_")
    ds = xr.open_dataset(f)
    if first:
        print(ds)   # check the variable is t2m and whether the time axis is "valid_time" or "time"
        first = False
    tcol = "valid_time" if "valid_time" in ds.coords else "time"

    # the file is already just the box, so average every cell in it
    df = ds["t2m"].mean(dim=["latitude", "longitude"]).to_dataframe().reset_index()
    df["year"] = df[tcol].dt.year
    df["temp_c"] = df["t2m"] - 273.15          # Kelvin to Celsius
    g = (df.groupby("year")
           .agg(temp_c=("temp_c", "mean"), months=("t2m", "count"))
           .reset_index())
    g["region"], g["country"] = r.region, r.country
    out.append(g)

res = pd.concat(out)
res.to_csv(PROCESSED / "era5_region_year.csv", index=False)
print(res.head(15))