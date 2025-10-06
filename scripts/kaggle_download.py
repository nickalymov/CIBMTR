import argparse
import os
import sys
from pathlib import Path

try:
	from kaggle import api as kaggle_api
except Exception as exc:
	print("Kaggle package is required. Install with: pip install kaggle", file=sys.stderr)
	raise

COMPETITION = "equity-post-HCT-survival-predictions"


def download_competition(destination: Path) -> None:
	"""Download core competition files into destination directory.

	The user must have accepted the competition rules and have Kaggle API configured.
	"""
	destination.mkdir(parents=True, exist_ok=True)
	# Files typically available: train.csv, test.csv, sample_submission.csv, data_dictionary.csv
	print(f"Downloading competition files to: {destination}")
	kaggle_api.competition_download_file(COMPETITION, "train.csv", path=str(destination), quiet=False)
	kaggle_api.competition_download_file(COMPETITION, "test.csv", path=str(destination), quiet=False)
	kaggle_api.competition_download_file(COMPETITION, "sample_submission.csv", path=str(destination), quiet=False)
	# optional dictionary if present
	try:
		kaggle_api.competition_download_file(COMPETITION, "data_dictionary.csv", path=str(destination), quiet=True)
	except Exception:
		pass

	# Unzip any downloaded zips if Kaggle returns zipped files
	for fname in os.listdir(destination):
		if fname.endswith(".zip"):
			zip_path = destination / fname
			print(f"Unzipping {zip_path} ...")
			import zipfile
			with zipfile.ZipFile(zip_path, "r") as zf:
				zf.extractall(destination)
			zip_path.unlink(missing_ok=True)


def main() -> None:
	parser = argparse.ArgumentParser(description="Download Kaggle competition data for CIBMTR post-HCT survival")
	parser.add_argument("--dest", type=str, default=str(Path("D.Data") / "main"), help="Destination directory for downloaded files")
	args = parser.parse_args()

	dest = Path(args.dest)
	download_competition(dest)
	print("Done.")


if __name__ == "__main__":
	main()
