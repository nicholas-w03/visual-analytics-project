from pathlib import Path
import kagglehub

scripts_dir = Path(__file__).resolve().parent
cqi_dir = scripts_dir.parent / "raw" / "cqi"
cqi_dir.mkdir(parents=True, exist_ok=True)
path = kagglehub.dataset_download("fatihb/coffee-quality-data-cqi", output_dir=cqi_dir)

print("Path to dataset files:", path)