from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def load_csv_to_sql(csv_path: str, table_name: str, database_url: str) -> int:
    engine = create_engine(database_url, future=True)
    df = pd.read_csv(csv_path)

    # Replace NaN with None for reliable SQL NULL insertion.
    df = df.where(pd.notna(df), None)

    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False, chunksize=5000)
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()

    return int(count)


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Load curated CSV into SQL")
    parser.add_argument(
        "--csv",
        default="data/processed/luxury_housing_sales_clean.csv",
    )
    parser.add_argument(
        "--table",
        default="luxury_housing_sales",
    )
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL"),
    )
    args = parser.parse_args()

    if not args.database_url:
        raise SystemExit("DATABASE_URL is not set. Copy .env.example to .env and configure it.")

    count = load_csv_to_sql(args.csv, args.table, args.database_url)
    print(f"Loaded {count:,} rows into {args.table}")


if __name__ == "__main__":
    main()
