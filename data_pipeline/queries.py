import sqlite3
from pathlib import Path


DATABASE_FILE = Path("data_pipeline/database/books.db")
OUTPUT_FILE = Path("data_pipeline/sql_results.txt")


def run_query(cursor, title, query):
    print(f"\n{'=' * 70}")
    print(title)
    print("=" * 70)
    print("SQL:")
    print(query)

    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nOutput:")
    for row in rows:
        print(row)

    return rows


def main():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    results = []

    # 1. SELECT + WHERE
    query1 = """
    SELECT title, price_gbp, rating
    FROM books
    WHERE rating >= 4;
    """
    results.append(
        run_query(
            cursor,
            "QUERY 1 - Books with rating >= 4",
            query1,
        )
    )

    # 2. ORDER BY
    query2 = """
    SELECT title, price_gbp
    FROM books
    ORDER BY price_gbp DESC;
    """
    results.append(
        run_query(
            cursor,
            "QUERY 2 - Books ordered by GBP price",
            query2,
        )
    )

    # 3. LIMIT
    query3 = """
    SELECT title, rating
    FROM books
    ORDER BY rating DESC
    LIMIT 10;
    """
    results.append(
        run_query(
            cursor,
            "QUERY 3 - Top 10 highest-rated books",
            query3,
        )
    )

    # 4. DISTINCT
    query4 = """
    SELECT DISTINCT category_name
    FROM categories
    ORDER BY category_name;
    """
    results.append(
        run_query(
            cursor,
            "QUERY 4 - Distinct categories",
            query4,
        )
    )

    # 5. BETWEEN
    query5 = """
    SELECT title, price_gbp
    FROM books
    WHERE price_gbp BETWEEN 20 AND 40
    ORDER BY price_gbp;
    """
    results.append(
        run_query(
            cursor,
            "QUERY 5 - Books priced between £20 and £40",
            query5,
        )
    )

    # 6. JOIN
    query6 = """
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
    results.append(
        run_query(
            cursor,
            "QUERY 6 - JOIN: Top-rated books with categories",
            query6,
        )
    )

    # Save query outputs.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for index, output_rows in enumerate(results, start=1):
            file.write(f"\nQUERY {index}\n")
            file.write("=" * 70 + "\n")

            for row in output_rows:
                file.write(str(row) + "\n")

    connection.close()

    print("\n" + "=" * 70)
    print("All SQL queries completed successfully.")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()