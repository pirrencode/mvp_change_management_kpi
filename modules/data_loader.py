from __future__ import annotations

from io import StringIO
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS: tuple[str, ...] = (
    "date",
    "department",
    "initiative",
    "adoption_rate",
    "training_completion",
    "engagement_sentiment",
    "communication_awareness",
    "readiness",
    "resistance_risk",
    "active_users",
    "target_users",
    "initiative_progress",
)


NUMERIC_COLUMNS: tuple[str, ...] = (
    "adoption_rate",
    "training_completion",
    "engagement_sentiment",
    "communication_awareness",
    "readiness",
    "resistance_risk",
    "active_users",
    "target_users",
    "initiative_progress",
)


def read_csv_file(uploaded_file, fallback_path: str) -> pd.DataFrame:
    """Read uploaded CSV file, or fallback to bundled sample data."""
    if uploaded_file is None:
        return pd.read_csv(fallback_path)

    data = uploaded_file.getvalue().decode("utf-8")
    return pd.read_csv(StringIO(data))


def validate_dataframe(df: pd.DataFrame, required_columns: Iterable[str] = REQUIRED_COLUMNS) -> list[str]:
    """Validate schema and return a list of human-readable errors."""
    errors: list[str] = []

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    if "date" in df.columns:
        parsed_dates = pd.to_datetime(df["date"], errors="coerce")
        invalid_dates = parsed_dates.isna().sum()
        if invalid_dates:
            errors.append(f"{invalid_dates} rows contain invalid dates in 'date'.")

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            coerced = pd.to_numeric(df[col], errors="coerce")
            invalid_num = coerced.isna().sum()
            if invalid_num:
                errors.append(f"{invalid_num} rows contain non-numeric values in '{col}'.")

    return errors


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize types and derive helper columns."""
    prepared = df.copy()
    prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")

    for col in NUMERIC_COLUMNS:
        prepared[col] = pd.to_numeric(prepared[col], errors="coerce")

    prepared = prepared.dropna(subset=["date", "department", "initiative"])
    prepared = prepared.sort_values("date")

    prepared["active_vs_target_pct"] = (prepared["active_users"] / prepared["target_users"]).replace([float("inf")], 0) * 100
    prepared["active_vs_target_pct"] = prepared["active_vs_target_pct"].fillna(0)

    return prepared
