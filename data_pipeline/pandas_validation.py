import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_FILE = Path("data_pipeline/database/books.db")
OUTPUT_FILE = Path("data_pipeline/pandas_validation.txt")


def main():
    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # ---------------------------------------------------------
    # PART 1: Read SQL query results into pandas
    # ---------------------------------------------------------

    query_1 = """
    SELECT title, price_gbp, rating
    FROM books
    WHERE rating >= 4;
    """

    query_5 = """
    SELECT title, price_gbp
    FROM books
    WHERE price_gbp BETWEEN 20 AND 40
    ORDER BY price_gbp;
    """

    query_6 = """
    SELECT
        books.title,
        categories.category_name,
        books.rating,
        books.price_gbp
    FROM books
    JOIN categories
        ON books.category_id = categories.category_id
    ORDER BY books.rating DESC, categories.category_name
    LIMIT 10;
    """

    df_query_1 = pd.read_sql(query_1, connection)
    df_query_5 = pd.read_sql(query_5, connection)
    df_sql_join = pd.read_sql(query_6, connection)

    print("=" * 70)
    print("QUERY 1 RESULT USING pd.read_sql()")
    print("=" * 70)
    print(df_query_1.head(10))

    print("\n")
    print("=" * 70)
    print("QUERY 5 RESULT USING pd.read_sql()")
    print("=" * 70)
    print(df_query_5.head(10))

    # ---------------------------------------------------------
    # PART 2: Reproduce the JOIN using pd.merge()
    # ---------------------------------------------------------

    df_books = pd.read_sql(
        """
        SELECT
            book_id,
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        FROM books;
        """,
        connection,
    )

    df_categories = pd.read_sql(
        """
        SELECT
            category_id,
            category_name
        FROM categories;
        """,
        connection,
    )

    # Perform the JOIN in pandas.
    df_merged = pd.merge(
        df_books,
        df_categories,
        on="category_id",
        how="inner",
    )

    # Match the columns and ordering used by SQL query 6.
    df_merged = df_merged[
        [
            "title",
            "category_name",
            "rating",
            "price_gbp",
        ]
    ]

    df_merged = df_merged.sort_values(
        by=["rating", "category_name"],
        ascending=[False, True],
    ).head(10)

    df_merged = df_merged.reset_index(drop=True)

    # Reset SQL JOIN result index for comparison.
    df_sql_join = df_sql_join.reset_index(drop=True)

    print("\n")
    print("=" * 70)
    print("SQL JOIN RESULT")
    print("=" * 70)
    print(df_sql_join)

    print("\n")
    print("=" * 70)
    print("pandas pd.merge() RESULT")
    print("=" * 70)
    print(df_merged)

    # ---------------------------------------------------------
    # PART 3: Check whether both outputs are equivalent
    # ---------------------------------------------------------

    equivalent = df_sql_join.equals(df_merged)

    print("\n")
    print("=" * 70)
    print("JOIN EQUIVALENCE CHECK")
    print("=" * 70)

    if equivalent:
        print("SQL JOIN and pandas pd.merge() outputs are equivalent: YES")
    else:
        print("SQL JOIN and pandas pd.merge() outputs are equivalent: NO")

    # ---------------------------------------------------------
    # PART 4: Save results for submission evidence
    # ---------------------------------------------------------

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("QUERY 1 - pd.read_sql()\n")
        file.write("=" * 70 + "\n")
        file.write(df_query_1.to_string(index=False))

        file.write("\n\nQUERY 5 - pd.read_sql()\n")
        file.write("=" * 70 + "\n")
        file.write(df_query_5.to_string(index=False))

        file.write("\n\nSQL JOIN RESULT\n")
        file.write("=" * 70 + "\n")
        file.write(df_sql_join.to_string(index=False))

        file.write("\n\npandas pd.merge() RESULT\n")
        file.write("=" * 70 + "\n")
        file.write(df_merged.to_string(index=False))

        file.write("\n\nEQUIVALENCE CHECK\n")
        file.write("=" * 70 + "\n")
        file.write(f"Equivalent: {equivalent}\n")

    connection.close()

    print(f"\nValidation results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()