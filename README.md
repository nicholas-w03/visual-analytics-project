# Is Climate Change Changing the Taste of Coffee?

*A Visual Analytics Approach to Origin Climate and Cupping Quality*

This is a group project for **Visual Analytics for Business Intelligence**. We examine how climate conditions at coffee-growing origins relate to Arabica flavor profiles, and present the findings in an interactive Tableau dashboard.

## Project Overview

- **Goal:** explore the relationship between origin climate (temperature, precipitation, altitude) and coffee cupping scores.
- **Deliverable:** an interactive dashboard. Statistical analysis serves as an intermediate step in the pipeline, not a standalone output.
- **Approach:** an iterative workflow with a feedback loop between data preparation, analysis and visualization.

## Data Sources

| Dataset | Content | Source |
|---|---|---|
| **CQI**, Arabica | Lot-level cupping scores, origin, altitude, variety, processing method | Coffee Quality Institute, Kaggle: `erwinhmtang/coffee-quality-institute-reviews-may2023` |
| **FAO** | Coffee production statistics by country and year | UN Food and Agriculture Organization, Kaggle: `junkochida/faostat-coffee-production-data-1961-2022` |
| **CHIRPS** | Gridded precipitation | Climate Hazards Group |
| **ERA5** | Gridded temperature (reanalysis) | Copernicus Climate Data Store |
| **ICO** | Coffee price by type and year | International Coffee Organisation, Kaggle: `yamaerenay/ico-coffee-dataset-worldwide` |

Country of origin is the common join key. The gridded climate data (CHIRPS, ERA5) is aggregated to country level before joining.

## Tools

- **Python:** data retrieval, cleaning, aggregation and analysis
- **Tableau:** interactive dashboard
- **Excel:** supplementary pre-analysis validation

## Repository Structure

```
.
├── data/
│   ├── scripts/             # downloads datasets into data/raw or data/processed
│   ├── raw/                 # downloaded data (gitignored, re-created by scripts)
│   └── processed/           # cleaned outputs, e.g. cqi_clean.csv
├── notebooks/               # CQI exploration and cleaning    
├── requirements.txt
└── README.md
```

## Setup

Requires Python 3.12.

```bash
# create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the repo root with your API credentials (the Copernicus CDS API for ERA5, and Kaggle if required). See `data/scripts/fetch_era5.py` for the expected variable names. Do not commit this file.

## Getting the Data

```bash
python data/scripts/<script_name>.py
```

This downloads the raw datasets into `data/raw/`.

## Acknowledgements

Data credit to the Coffee Quality Institute,  (Kaggle dataset), the FAO, the Climate Hazards Group (CHIRPS) and the Copernicus Climate Change Service (ERA5).