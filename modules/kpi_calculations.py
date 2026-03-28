from __future__ import annotations

import pandas as pd

PERCENT_KPI_COLUMNS = [
    "adoption_rate",
    "training_completion",
    "engagement_sentiment",
    "communication_awareness",
    "readiness",
    "initiative_progress",
    "active_vs_target_pct",
]


def _safe_mean(series: pd.Series) -> float:
    if series.empty:
        return 0.0
    return float(series.mean())


def get_latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Return only rows at latest date in filtered data."""
    if df.empty:
        return df
    latest_date = df["date"].max()
    return df[df["date"] == latest_date]


def compute_summary_metrics(df: pd.DataFrame) -> dict[str, float]:
    """Compute top-level KPI values for KPI cards."""
    snapshot = get_latest_snapshot(df)

    metrics = {
        "Adoption Rate": _safe_mean(snapshot["adoption_rate"]),
        "Training Completion": _safe_mean(snapshot["training_completion"]),
        "Engagement / Sentiment": _safe_mean(snapshot["engagement_sentiment"]),
        "Communication Awareness": _safe_mean(snapshot["communication_awareness"]),
        "Readiness": _safe_mean(snapshot["readiness"]),
        "Resistance / Risk": _safe_mean(snapshot["resistance_risk"]),
        "Active vs Target Users": _safe_mean(snapshot["active_vs_target_pct"]),
        "Initiative Progress": _safe_mean(snapshot["initiative_progress"]),
    }

    return metrics


def time_series_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Return time-series trend table for selected KPIs."""
    if df.empty:
        return pd.DataFrame()

    trend = (
        df.groupby("date", as_index=False)[
            [
                "adoption_rate",
                "training_completion",
                "engagement_sentiment",
                "communication_awareness",
                "readiness",
                "resistance_risk",
                "active_vs_target_pct",
                "initiative_progress",
            ]
        ]
        .mean()
        .sort_values("date")
    )
    return trend


def department_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Average KPI performance by department for comparison charts."""
    if df.empty:
        return pd.DataFrame()

    dept = (
        df.groupby("department", as_index=False)[
            [
                "adoption_rate",
                "training_completion",
                "engagement_sentiment",
                "communication_awareness",
                "readiness",
                "resistance_risk",
                "initiative_progress",
                "active_vs_target_pct",
            ]
        ]
        .mean()
        .sort_values("adoption_rate", ascending=False)
    )
    return dept


def initiative_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Get latest initiative-level details for risk/progress tracking."""
    snapshot = get_latest_snapshot(df)
    if snapshot.empty:
        return pd.DataFrame()

    table = (
        snapshot.groupby(["initiative", "department"], as_index=False)[
            [
                "initiative_progress",
                "resistance_risk",
                "adoption_rate",
                "training_completion",
                "active_users",
                "target_users",
                "active_vs_target_pct",
            ]
        ]
        .mean()
        .sort_values(["resistance_risk", "initiative_progress"], ascending=[False, True])
    )
    return table
