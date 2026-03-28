from __future__ import annotations

import streamlit as st

from modules.charts import (
    department_bar_chart,
    donut_progress_chart,
    line_trend_chart,
    risk_heatmap,
)
from modules.data_loader import prepare_dataframe, read_csv_file, validate_dataframe
from modules.kpi_calculations import (
    compute_summary_metrics,
    department_comparison,
    initiative_snapshot,
    time_series_kpis,
)

st.set_page_config(
    page_title="Change Management KPI Dashboard",
    page_icon="📈",
    layout="wide",
)

SAMPLE_DATA_PATH = "data/sample_change_management_data.csv"


def format_metric(name: str, value: float) -> str:
    if name == "Resistance / Risk":
        return f"{value:.2f} / 5"
    return f"{value:.1f}%"


def show_empty_state(message: str) -> None:
    st.info(message)
    st.stop()


st.title("📈 Change Management Dashboard")
st.caption("Demo-ready MVP for tracking digital transformation change KPIs.")

with st.sidebar:
    st.header("Data & Filters")
    uploaded_file = st.file_uploader("Upload CSV data", type=["csv"])

raw_df = read_csv_file(uploaded_file, SAMPLE_DATA_PATH)
validation_errors = validate_dataframe(raw_df)

if validation_errors:
    st.error("We found issues in the uploaded data. Please fix the file and try again.")
    for err in validation_errors:
        st.write(f"• {err}")
    st.stop()


df = prepare_dataframe(raw_df)
if df.empty:
    show_empty_state("No valid rows available after processing. Please upload a complete dataset.")

with st.sidebar:
    departments = ["All"] + sorted(df["department"].unique().tolist())
    initiatives = ["All"] + sorted(df["initiative"].unique().tolist())

    selected_dept = st.selectbox("Department", departments)
    selected_initiative = st.selectbox("Initiative", initiatives)

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

filtered = df.copy()
if selected_dept != "All":
    filtered = filtered[filtered["department"] == selected_dept]
if selected_initiative != "All":
    filtered = filtered[filtered["initiative"] == selected_initiative]
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[(filtered["date"].dt.date >= start_date) & (filtered["date"].dt.date <= end_date)]

if filtered.empty:
    show_empty_state("No rows match the selected filters. Adjust filters to continue.")

summary_metrics = compute_summary_metrics(filtered)
trend_df = time_series_kpis(filtered)
dept_df = department_comparison(filtered)
initiative_df = initiative_snapshot(filtered)

section = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "KPI Trends",
        "Department Comparison",
        "Initiative Details",
        "Data Table",
    ],
)

if section == "Executive Summary":
    st.subheader("Executive Summary")
    cols = st.columns(4)
    metric_items = list(summary_metrics.items())
    for idx, (label, value) in enumerate(metric_items):
        cols[idx % 4].metric(label, format_metric(label, value))

    c1, c2 = st.columns([1, 1])
    with c1:
        st.plotly_chart(donut_progress_chart(initiative_df), use_container_width=True)
    with c2:
        if not initiative_df.empty:
            top_risk = initiative_df.nlargest(5, "resistance_risk")[
                ["initiative", "department", "resistance_risk", "initiative_progress"]
            ]
            st.markdown("**Top 5 Risk Initiatives**")
            st.dataframe(top_risk, use_container_width=True, hide_index=True)
        else:
            st.info("No initiative-level snapshot available for current filters.")

elif section == "KPI Trends":
    st.subheader("KPI Trends")
    if trend_df.empty:
        show_empty_state("No trend data available for the selected scope.")

    metric_options = [
        "adoption_rate",
        "training_completion",
        "engagement_sentiment",
        "communication_awareness",
        "readiness",
        "resistance_risk",
        "active_vs_target_pct",
        "initiative_progress",
    ]
    selected_metric = st.selectbox("Trend KPI", metric_options, index=0)
    st.plotly_chart(line_trend_chart(trend_df, selected_metric), use_container_width=True)

elif section == "Department Comparison":
    st.subheader("Department Comparison")
    if dept_df.empty:
        show_empty_state("No department data available for the selected scope.")

    metric_options = [
        "adoption_rate",
        "training_completion",
        "engagement_sentiment",
        "communication_awareness",
        "readiness",
        "resistance_risk",
        "initiative_progress",
        "active_vs_target_pct",
    ]
    selected_metric = st.selectbox("Comparison KPI", metric_options, index=0)
    st.plotly_chart(department_bar_chart(dept_df, selected_metric), use_container_width=True)

elif section == "Initiative Details":
    st.subheader("Initiative Details")
    if initiative_df.empty:
        show_empty_state("No initiative details available for the selected scope.")

    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.plotly_chart(risk_heatmap(initiative_df), use_container_width=True)
    with c2:
        st.markdown("**Risk & Progress Table**")
        st.dataframe(
            initiative_df[
                [
                    "initiative",
                    "department",
                    "resistance_risk",
                    "initiative_progress",
                    "adoption_rate",
                    "training_completion",
                    "active_vs_target_pct",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

elif section == "Data Table":
    st.subheader("Data Table")
    st.caption("Filtered dataset used to calculate all KPIs and charts.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption(
    "Tip: Upload your own CSV with the sample schema to demo different program scenarios."
)
