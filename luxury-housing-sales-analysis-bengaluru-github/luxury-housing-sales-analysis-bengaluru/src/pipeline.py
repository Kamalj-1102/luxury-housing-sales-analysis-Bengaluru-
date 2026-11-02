from __future__ import annotations

import argparse
from pathlib import Path

from .cleaning import clean_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Luxury housing ETL pipeline")
    parser.add_argument("--input", required=True, help="Raw CSV path")
    parser.add_argument(
        "--output",
        default="data/processed/luxury_housing_sales_clean.csv",
        help="Cleaned CSV output",
    )
    parser.add_argument(
        "--report",
        default="data/processed/data_quality_report.csv",
        help="Data quality report output",
    )
    args = parser.parse_args()

    df = clean_csv(args.input, args.output, args.report)
    print(f"ETL complete: {len(df):,} rows written to {args.output}")
    print(f"Quality report written to {args.report}")


if __name__ == "__main__":
    main()
