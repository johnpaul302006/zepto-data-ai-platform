import re

import pandas as pd


INPUT_FILE = "data_pipeline/raw_books.csv"
OUTPUT_FILE = "data_pipeline/cleaned_books.csv"

GBP_TO_INR = 105.50

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_price(value):
    """Convert GBP price text into a float."""
    if pd.isna(value):
        return None

    # Handles values such as Â£51.77 or £51.77.
    cleaned = re.sub(r"[^0-9.]", "", str(value))

    try:
        return float(cleaned)
    except ValueError:
        return None


def clean_rating(value):
    """Convert text star rating into an integer from 1 to 5."""
    if pd.isna(value):
        return None

    return RATING_MAP.get(str(value).strip())


def clean_stock(value):
    """Convert availability text into a boolean."""
    if pd.isna(value):
        return None

    text = str(value).strip().lower()

    if "in stock" in text:
        return True

    if "out of stock" in text:
        return False

    return None


def main():
    df = pd.read_csv(INPUT_FILE)

    print("Raw rows:", len(df))

    # Clean required fields.
    df["price_gbp"] = df["price"].apply(clean_price)
    df["rating"] = df["star_rating"].apply(clean_rating)
    df["in_stock"] = df["availability"].apply(clean_stock)

    # Handle numeric parsing failures with median imputation.
    price_median = df["price_gbp"].median()
    rating_median = df["rating"].median()

    df["price_gbp"] = df["price_gbp"].fillna(price_median)
    df["rating"] = df["rating"].fillna(rating_median).round().astype(int)

    # If stock parsing fails, drop those rows because the field cannot
    # be safely inferred as True/False.
    invalid_stock = df["in_stock"].isna().sum()

    if invalid_stock > 0:
        print(f"Dropping {invalid_stock} rows with unparseable availability.")
        df = df.dropna(subset=["in_stock"])

    df["in_stock"] = df["in_stock"].astype(bool)

    # Required fixed project conversion rate.
    df["price_inr"] = df["price_gbp"] * GBP_TO_INR

    # Keep only the cleaned/project-required columns.
    cleaned_df = df[
        [
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category",
        ]
    ].copy()

    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    print("\n========== CLEANING COMPLETE ==========")
    print("Cleaned rows:", len(cleaned_df))
    print("Columns:", cleaned_df.columns.tolist())

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nFirst 5 cleaned rows:")
    print(cleaned_df.head())

    print(f"\nSaved to: {OUTPUT_FILE}")
    print(f"GBP to INR rate used: {GBP_TO_INR}")


if __name__ == "__main__":
    main()