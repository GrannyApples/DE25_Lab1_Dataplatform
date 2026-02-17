from pathlib import Path
from ingest import csv_to_json
from transform import clean_data
from analyze import run_analysis

##Did this because it couldnt find the path after using src/main.py, most likely directory issue when i added the folders,
# so py cant find the actual path. Did make it work with a hardcoded path, but that looked ugly = r"C:\Users\user\code\Dataplatform-Lab1-Anton-E\data\raw\products.csv"
## so i did some checking of how to setup a hard path, found this option. and it works...
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

if __name__ == '__main__':
    ##Ingest function to take the raw file and give me a processed json according to pdf instructions.
    raw_csv = RAW_DIR / "products.csv"
    processed_json = PROCESSED_DIR / "products.json"
    rejected_json = PROCESSED_DIR / "rejected.json"

    csv_to_json(raw_csv, processed_json)
    ##Using the transform function to filter out what is needed according to the pdf file.
    clea_df, rejected_df = clean_data(processed_json)
    ##data/processed/rejected.json, is the same as outputs, just using pydantic.
    rejected_df.to_json(rejected_json, orient="records", indent=2)

    run_analysis(clea_df)