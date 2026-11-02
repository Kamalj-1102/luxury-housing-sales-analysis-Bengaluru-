from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ALIASES = {
    "project_id": ["project_id", "projectid", "project id"],
    "micro_market": ["micro_market", "micro market", "micromarket", "locality"],
    "builder": ["builder", "developer", "builder_name"],
    "ticket_price_cr": ["ticket_price_cr", "ticket price cr", "ticket_price", "price_cr"],
    "configuration": ["configuration", "config", "unit_configuration"],
    "possession_status": ["possession_status", "possession status", "possession"],
    "amenity_score": ["amenity_score", "amenity score", "amenity_rating"],
    "booking_status": ["booking_status", "booking status", "status"],
    "purchase_quarter": ["purchase_quarter", "purchase quarter", "quarter", "purchase_qtr"],
    "sales_channel": ["sales_channel", "sales channel", "channel"],
    "buyer_type": ["buyer_type", "buyer type", "customer_type"],
    "buyer_comments": ["buyer_comments", "buyer comments", "comments", "comment"],
}

REQUIRED = ["project_id", "micro_market", "builder", "ticket_price_cr", "booking_status"]


def _key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    normalized = {_key(c): c for c in df.columns}
    rename = {}
    for target, candidates in ALIASES.items():
        for candidate in candidates:
            if _key(candidate) in normalized:
                rename[normalized[_key(candidate)]] = target
                break
    return df.rename(columns=rename)


def clean_numeric(series: pd.Series) -> pd.Series:
    # Handles values such as "₹12.50 Cr", "12.5", "12,50", or blanks.
    return pd.to_numeric(
        series.astype("string")
        .str.replace(",", "", regex=False)
        .str.replace(r"[₹$]", "", regex=True)
        .str.replace(r"\bcr\b", "", regex=True, case=False)
        .str.strip(),
        errors="coerce",
    )


def normalize_text(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    )


def derive_quarter_number(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.upper()
    extracted = pd.to_numeric(text.str.extract(r"([1-4])")[0], errors="coerce")
    return extracted.astype("Int64")


def derive_booking_flag(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.lower().str.strip()
    booked = text.isin({"booked", "booking", "confirmed", "sold", "successful", "yes", "1"})
    return booked.astype("int8")


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)

    for col in ["project_id", "micro_market", "builder", "configuration",
                "possession_status", "booking_status", "purchase_quarter",
                "sales_channel", "buyer_type", "buyer_comments"]:
        if col in df.columns:
            df[col] = normalize_text(df[col])

    if "ticket_price_cr" in df.columns:
        df["ticket_price_cr"] = clean_numeric(df["ticket_price_cr"])

    if "amenity_score" in df.columns:
        df["amenity_score"] = clean_numeric(df["amenity_score"])

    if "ticket_price_cr" in df.columns:
        # Price per sqft is only calculated if a usable area column exists.
        area_candidates = [c for c in df.columns if _key(c) in {
            "area_sqft", "carpet_area_sqft", "built_up_area_sqft",
            "saleable_area_sqft", "super_built_up_area_sqft"
        }]
        if area_candidates:
            area_col = area_candidates[0]
            df["area_sqft"] = clean_numeric(df[area_col])
            df["price_per_sqft"] = np.where(
                df["area_sqft"] > 0,
                (df["ticket_price_cr"] * 10_000_000) / df["area_sqft"],
                np.nan,
            )

    if "purchase_quarter" in df.columns:
        df["quarter_number"] = derive_quarter_number(df["purchase_quarter"])

    if "booking_status" in df.columns:
        df["booking_flag"] = derive_booking_flag(df["booking_status"])

    # Keep duplicate Project_ID rows if they represent transactions; only remove
    # exact duplicate records.
    df = df.drop_duplicates().reset_index(drop=True)

    return df


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "row_count": [len(df)] * len(df.columns),
        "missing_count": [int(df[c].isna().sum()) for c in df.columns],
        "missing_pct": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "unique_count": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    return report


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns after standardization: {missing}. "
            f"Available columns: {list(df.columns)}"
        )


def clean_csv(input_path: str | Path, output_path: str | Path,
               report_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    cleaned = clean_dataset(df)
    validate_required_columns(cleaned)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    quality_report(cleaned).to_csv(report_path, index=False)
    return cleaned
