# Change Management KPI Dashboard (MVP)

A demo-ready Streamlit MVP for digital transformation change-management reporting. This project is designed for leaders and program managers who need fast, clear visibility into adoption, readiness, risk, and initiative performance.

## Features

- **Executive Summary** with KPI cards and progress donut
- **KPI Trends** over time (line charts)
- **Department Comparison** (bar chart)
- **Initiative Details** with risk heatmap + details table
- **Data Table** for full filtered dataset
- CSV upload support with schema validation and clear empty/error states
- Runs locally and is compatible with **Streamlit Community Cloud**

## KPI Coverage

This MVP visualizes:

- Adoption rate
- Training completion
- Engagement / sentiment
- Communication awareness
- Readiness
- Resistance / risk
- Active vs target users
- Initiative progress

## Repository Structure

```text
.
├── app.py
├── modules/
│   ├── __init__.py
│   ├── charts.py
│   ├── data_loader.py
│   └── kpi_calculations.py
├── data/
│   └── sample_change_management_data.csv
├── requirements.txt
└── README.md
```

## Expected CSV Schema

The app expects these columns:

- `date`
- `department`
- `initiative`
- `adoption_rate`
- `training_completion`
- `engagement_sentiment`
- `communication_awareness`
- `readiness`
- `resistance_risk`
- `active_users`
- `target_users`
- `initiative_progress`

> Percent-style metrics use a 0–100 scale. `resistance_risk` uses 1–5.

## Run Locally

1. Clone repo:
   ```bash
   git clone <your-repo-url>
   cd mvp_change_management_kpi
   ```
2. Create and activate a virtual environment (recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run Streamlit:
   ```bash
   streamlit run app.py
   ```
5. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from your repo.
3. Set:
   - **Main file path**: `app.py`
   - **Python dependencies**: `requirements.txt` (auto-detected)
4. Deploy.

## Notes for Future Enterprise Integration

- Modularized into data loading, KPI calculations, and chart utilities for easy replacement with API/database backends.
- Validation layer is isolated and can be extended with stricter quality checks.
- Current sample data can be replaced with secure connectors (e.g., warehouse, HRIS, LMS, comms platform) with minimal UI changes.

## Demo Tips

- Start with bundled sample data for a stable demo.
- Use sidebar filters to simulate leader views by department/initiative/date.
- Upload alternative CSVs to demonstrate scenario-based storytelling.
