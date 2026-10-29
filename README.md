# AI-Powered Business Analyst Copilot

A portfolio project for Business Analyst and Data Analyst roles, built with Python, Streamlit, pandas, Plotly, and SQLite.

## Features
- Executive KPIs: gross sales, net revenue, order count, return rate, fees, and estimated profit.
- Monthly and category sales visualisations.
- CSV/Excel upload and interactive filters.
- Rule-based questions about products, categories, sales trends, and returns.
- Read-only SQLite SQL explorer.
- Basic data-quality checks and filtered CSV download.

> The current question-answering module is rule-based, not connected to a generative AI API. The included dataset is synthetic and must not be presented as real company data.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Tech stack
Python, Streamlit, pandas, Plotly, SQLite, SQL.

## Metric notes
- Recorded return rate = returned rows / non-cancelled rows. This is a demo definition, not necessarily a unit- or value-based return rate.
- Estimated profit = net revenue - estimated product cost - marketplace fees - shipping cost.
- Validate business definitions, refunds, taxes, and fee reversals before using real business data.

## Portfolio summary
Built an interactive analytics application that loads CSV/Excel data, calculates business KPIs, visualises trends, supports common analytical questions, offers a read-only SQL interface, and flags data-quality issues. Next steps include schema mapping, a PostgreSQL connector, and securely grounded LLM answers with SQL validation.
