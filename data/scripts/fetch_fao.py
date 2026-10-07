from pathlib import Path
import kagglehub

scripts_dir = Path(__file__).resolve().parent
fao_dir = scripts_dir.parent / "raw" / "fao"
fao_dir.mkdir(parents=True, exist_ok=True)
path = kagglehub.dataset_download("junkochida/faostat-coffee-production-data-1961-2022", output_dir=fao_dir)

print("Path to dataset files:", path)