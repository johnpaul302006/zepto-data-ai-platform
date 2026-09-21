import sqlite3
from pathlib import Path

import pandas as pd


CLEANED_FILE = "data_pipeline/cleaned_books.csv"
DATABASE_DIR = Path("data_pipeline/database")
DATABASE_FILE = DATABASE_DIR / "books.db"


def create_database():
    # Create the database folder if it does not exist.
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Read cleaned data.
    df = pd.read_csv(CLEANED_FILE)

    # Connect to SQLite.
    connection = sqlite3.connect(DATABASE_FILE)

    # Enable foreign-key enforcement.
    connection.execute("PRAGMA foreign_keys = ON")

    cursor = connection.cursor()

    # Remove old tables if they already exist.
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS categories")

    # Create categories table.
    cursor.execute(
        """
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
        """
    )

    # Create books table.
    cursor.execute(
        """
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL NOT NULL,
            price_inr REAL NOT NULL,
            rating INTEGER NOT NULL,
            in_stock INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
        """
    )

    # Insert unique categories.
    categories = sorted(df["category"].dropna().unique())

    for category in categories:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category,),
        )

    # Create category -> category_id mapping.
    category_rows = cursor.execute(
        "SELECT category_id, category_name FROM categories"
    ).fetchall()

    category_map = {
        category_name: category_id
        for category_id, category_name in category_rows
    }

    # Insert books.
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO books (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                int(row["rating"]),
                int(row["in_stock"]),
                category_map[row["category"]],
            ),
        )

    connection.commit()

    # Show counts for verification.
    category_count = cursor.execute(
        "SELECT COUNT(*) FROM categories"
    ).fetchone()[0]

    book_count = cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    print("========== DATABASE CREATED ==========")
    print("Database:", DATABASE_FILE)
    print("Categories:", category_count)
    print("Books:", book_count)

    # Verify foreign-key relationship.
    foreign_keys = cursor.execute(
        "PRAGMA foreign_key_list(books)"
    ).fetchall()

    print("\nForeign key definition:")
    print(foreign_keys)

    connection.close()


if __name__ == "__main__":
    create_database()