import pandas as pd
from pathlib import Path

##just like i did in main.py to grab the file, same issue as in main.py.
#could make a fixture/helper for this since its used in 2 places to follow DRY principles.
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_DIR = BASE_DIR / "data" / "outputs"

def run_analysis(clean_df: pd.DataFrame, rejected_df: pd.DataFrame):
    ANALYTICS_SUMMARY = PATH_DIR / "analytics_summary.json"
    PRICE_ANALYSIS = PATH_DIR / "price_analysis.json"
    REJECTED_ANALYSIS = PATH_DIR / "rejected_products.json"

    clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")
    rejected_df["price"] = pd.to_numeric(rejected_df["price"], errors="coerce")
    full_df = pd.concat([clean_df, rejected_df], ignore_index=True)

    ##Ensure prices are numeric, need this check to grab the missing price count, before validation or anything else.
    full_df["price"] = pd.to_numeric(full_df["price"], errors="coerce")

    summary = pd.DataFrame({
        "average_price": [full_df["price"].mean()],
        "median_price": [full_df["price"].median()],
        "product_count": [len(full_df)],
        "missing_price_count": [full_df["price"].isna().sum()]
    })


    summary.to_json(ANALYTICS_SUMMARY, orient="records", indent=2)

    top_expensive = clean_df.nlargest(10, "price")
    top_expensive.to_json(PRICE_ANALYSIS, orient="records", indent=2)

    rejected_df.to_json(REJECTED_ANALYSIS, orient="records", indent=2)
