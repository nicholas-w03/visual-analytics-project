from pathlib import Path
import kagglehub

scripts_dir = Path(__file__).resolve().parent
cqi_dir = scripts_dir.parent / "raw" / "ico"
cqi_dir.mkdir(parents=True, exist_ok=True)
path = kagglehub.dataset_download("yamaerenay/ico-coffee-dataset-worldwide", output_dir=cqi_dir)

print("Path to dataset files:", path)