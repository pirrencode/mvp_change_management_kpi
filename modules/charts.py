from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def line_trend_chart(trend_df: pd.DataFrame, metric: str) -> go.Figure:
    fig = px.line(
        trend_df,
        x="date",
        y=metric,
        title=f"{metric.replace('_', ' ').title()} Trend",
        markers=True,
    )
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=55, b=20))
    fig.update_yaxes(range=[0, 100] if metric != "resistance_risk" else [0, 5])
    return fig


def department_bar_chart(dept_df: pd.DataFrame, metric: str) -> go.Figure:
    fig = px.bar(
        dept_df,
        x="department",
        y=metric,
        color=metric,
        color_continuous_scale="Blues",
        title=f"Department Comparison: {metric.replace('_', ' ').title()}",
    )
    fig.update_layout(height=360, margin=dict(l=20, r=20, t=55, b=20), coloraxis_showscale=False)
    fig.update_yaxes(range=[0, 100] if metric != "resistance_risk" else [0, 5])
    return fig


def donut_progress_chart(snapshot_df: pd.DataFrame) -> go.Figure:
    avg_progress = float(snapshot_df["initiative_progress"].mean()) if not snapshot_df.empty else 0.0
    remaining = max(0, 100 - avg_progress)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Progress", "Remaining"],
                values=[avg_progress, remaining],
                hole=0.65,
                marker=dict(colors=["#1f77b4", "#d9e6f2"]),
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(
        title="Overall Initiative Progress",
        annotations=[dict(text=f"{avg_progress:.1f}%", x=0.5, y=0.5, showarrow=False, font_size=20)],
        height=320,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def risk_heatmap(initiative_df: pd.DataFrame) -> go.Figure:
    if initiative_df.empty:
        return go.Figure()

    fig = px.scatter(
        initiative_df,
        x="initiative_progress",
        y="resistance_risk",
        color="department",
        size="active_vs_target_pct",
        hover_name="initiative",
        size_max=35,
        title="Risk Heatmap (Risk vs Progress)",
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=55, b=20))
    fig.update_xaxes(title="Initiative Progress (%)", range=[0, 100])
    fig.update_yaxes(title="Resistance / Risk (1-5)", range=[0, 5])
    return fig
