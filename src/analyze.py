import pandas as pd
from pathlib import Path

##just like i did in main.py to grab the file, same issue as in main.py.
#could make a fixture/helper for this since its used in 2 places to follow DRY principles.
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_DIR = BASE_DIR / "data" / "outputs"

def run_analysis(df):
    ANALYTICS_SUMMARY = PATH_DIR / "analytics_summary.json"
    PRICE_ANALYSIS = PATH_DIR / "price_analysis.json"
    REJECTED_ANALYSIS = PATH_DIR / "rejected_products.json"

    rejected = df[
        df["id"].isna() |
        df["name"].isna() |
        df["price"].isna() |
        (df["price"] < 0)
    ]

    clean = df.drop(rejected.index)

    summary = pd.DataFrame({
        "average_price": [clean["price"].mean()],
        "median_price": [clean["price"].median()],
        "product_count": [len(clean)],
        "missing_price_count": [df["price"].isna().sum()]
    })

    summary.to_json(ANALYTICS_SUMMARY, orient="records", indent=2)

    top_expensive = clean.nlargest(10, "price")
    top_expensive.to_json(PRICE_ANALYSIS, orient="records", indent=2)

    rejected.to_json(REJECTED_ANALYSIS, orient="records", indent=2)
