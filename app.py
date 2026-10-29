import re
import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "sample_ecommerce_orders.csv"
st.set_page_config(page_title="Business Analyst Copilot", page_icon="📊", layout="wide")
st.title("🤖 AI-Powered Business Analyst Copilot")
st.caption("Explore business KPIs, trends, returns, and data quality. Sample data is synthetic.")

with st.sidebar:
    st.header("Data workspace")
    upload = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    st.info("Use only data you are authorized to upload. Avoid confidential or personal data in public demos.")

@st.cache_data
def sample_data():
    return pd.read_csv(DATA_PATH, parse_dates=["order_date"])

try:
    df = (pd.read_csv(upload) if upload and upload.name.lower().endswith(".csv")
          else pd.read_excel(upload) if upload else sample_data())
except Exception as exc:
    st.error("Could not read file: " + str(exc))
    st.stop()

df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
if not {"order_date", "gross_sales"}.issubset(df.columns):
    st.error("Dataset must include order_date and gross_sales columns.")
    st.stop()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
for col in ["gross_sales", "net_revenue", "estimated_profit", "refund_amount", "marketplace_fee", "quantity"]:
    if col in df:
        df[col] = pd.to_numeric(df[col], errors="coerce")
for col, fallback in [("order_status", "Unknown"), ("category", "Uncategorised"), ("product_name", "Unknown product"), ("return_reason", "")]:
    if col not in df:
        df[col] = fallback
if "net_revenue" not in df:
    df["net_revenue"] = df["gross_sales"]
if "marketplace_fee" not in df:
    df["marketplace_fee"] = 0
if "refund_amount" not in df:
    df["refund_amount"] = 0

status = df["order_status"].fillna("").astype(str).str.lower()
returned = status.str.contains("return", na=False)
cancelled = status.str.contains("cancel", na=False)
valid_orders = int((~cancelled).sum())
return_rate = int(returned.sum()) / max(valid_orders, 1)
gross = float(df["gross_sales"].fillna(0).sum())
net = float(df["net_revenue"].fillna(0).sum())
fees = float(df["marketplace_fee"].fillna(0).sum())
profit = float(df["estimated_profit"].fillna(0).sum()) if "estimated_profit" in df and df["estimated_profit"].notna().any() else None

overview, explore, ask, sqltab, quality = st.tabs(["Overview", "Explore", "Ask the data", "SQL explorer", "Data quality"])
with overview:
    st.subheader("Executive overview")
    a, b, c, d = st.columns(4)
    a.metric("Gross sales", "₹{:,.0f}".format(gross))
    b.metric("Net revenue", "₹{:,.0f}".format(net))
    c.metric("Orders excl. cancelled", "{:,}".format(valid_orders))
    d.metric("Recorded return rate", "{:.1%}".format(return_rate))
    e, f = st.columns(2)
    e.metric("Marketplace fees", "₹{:,.0f}".format(fees))
    if profit is not None:
        f.metric("Estimated profit", "₹{:,.0f}".format(profit))
    dated = df.dropna(subset=["order_date"]).copy()
    if not dated.empty:
        dated["month"] = dated["order_date"].dt.to_period("M").astype(str)
        monthly = dated.groupby("month", as_index=False).agg(gross_sales=("gross_sales", "sum"), net_revenue=("net_revenue", "sum"))
        left, right = st.columns(2)
        left.plotly_chart(px.line(monthly, x="month", y=["gross_sales", "net_revenue"], markers=True, title="Monthly sales and revenue"), use_container_width=True)
        by_cat = df.groupby("category", as_index=False)["gross_sales"].sum().sort_values("gross_sales", ascending=False)
        right.plotly_chart(px.bar(by_cat, x="category", y="gross_sales", title="Sales by category"), use_container_width=True)
    st.warning("Synthetic demo data. Validate metric definitions before using results for decisions.")

with explore:
    st.subheader("Filter and inspect records")
    filtered = df.copy()
    cols = st.columns(3)
    for idx, col in enumerate(["category", "channel", "order_status"]):
        if col in filtered:
            opts = sorted(filtered[col].fillna("Unknown").astype(str).unique())
            chosen = cols[idx].multiselect(col.replace("_", " ").title(), opts, default=opts)
            filtered = filtered[filtered[col].fillna("Unknown").astype(str).isin(chosen)]
    st.write("{} rows match your filters.".format(len(filtered)))
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_data.csv", "text/csv")

with ask:
    st.subheader("Ask the data")
    st.caption("This starter uses rule-based analysis; it is not yet connected to a generative AI model.")
    question = st.text_input("Ask a question", placeholder="e.g. Which categories have the highest sales?")
    if st.button("Analyse", type="primary", disabled=not question.strip()):
        q = question.lower()
        if "return reason" in q or ("why" in q and "return" in q):
            result = df[df["return_reason"].astype(str).str.strip().ne("")]["return_reason"].value_counts().rename_axis("return_reason").reset_index(name="count")
            st.dataframe(result, use_container_width=True, hide_index=True)
        elif "return" in q:
            st.write("Recorded return rate: {:.1%} ({} returned rows / {} non-cancelled rows).".format(return_rate, int(returned.sum()), valid_orders))
            if "category" in q:
                temp = df.assign(_return=returned, _valid=~cancelled).groupby("category", as_index=False).agg(returns=("_return", "sum"), orders=("_valid", "sum"))
                temp["return_rate"] = temp["returns"] / temp["orders"].replace(0, pd.NA)
                st.dataframe(temp.sort_values("return_rate", ascending=False), use_container_width=True, hide_index=True)
        elif "month" in q or "trend" in q:
            dated = df.dropna(subset=["order_date"]).copy()
            dated["month"] = dated["order_date"].dt.to_period("M").astype(str)
            st.dataframe(dated.groupby("month", as_index=False)["gross_sales"].sum(), use_container_width=True, hide_index=True)
        elif "categor" in q:
            st.dataframe(df.groupby("category", as_index=False)["gross_sales"].sum().sort_values("gross_sales", ascending=False), use_container_width=True, hide_index=True)
        elif any(word in q for word in ["product", "item", "sku"]):
            result = df.groupby("product_name", as_index=False)["gross_sales"].sum().sort_values("gross_sales", ascending=("lowest" in q or "bottom" in q))
            st.dataframe(result.head(5), use_container_width=True, hide_index=True)
        elif any(word in q for word in ["summary", "summarise", "overview", "dataset"]):
            st.write("{} rows, {} columns; gross sales ₹{:,.2f}; net revenue ₹{:,.2f}; recorded return rate {:.1%}.".format(len(df), len(df.columns), gross, net, return_rate))
        else:
            st.info("Try: dataset summary, category sales, top products, monthly trend, return rate, or return reasons.")

with sqltab:
    st.subheader("Read-only SQL explorer")
    st.caption("Table name: business_data. Only SELECT statements are permitted.")
    query = st.text_area("SQL query", value="SELECT category, SUM(gross_sales) AS sales FROM business_data GROUP BY category ORDER BY sales DESC LIMIT 20", height=110)
    con = sqlite3.connect(":memory:")
    df.to_sql("business_data", con, index=False, if_exists="replace")
    if st.button("Run SQL"):
        clean = query.strip().rstrip(";")
        if not re.match(r"(?is)^select\b", clean) or ";" in clean or re.search(r"(?i)\b(insert|update|delete|drop|alter|create|attach|detach|pragma|replace|vacuum|into)\b", clean):
            st.error("Only one read-only SELECT query is allowed.")
        else:
            try:
                st.dataframe(pd.read_sql_query(clean, con), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error("Query failed: " + str(exc))
    con.close()

with quality:
    st.subheader("Data quality checks")
    checks = [
        ("Duplicate rows", int(df.duplicated().sum()), "Review duplicate records."),
        ("Missing dates", int(df["order_date"].isna().sum()), "Check date parsing and completeness."),
        ("Negative gross sales", int((df["gross_sales"] < 0).sum()), "Confirm whether adjustments are expected."),
    ]
    for col in ["order_id", "product_name", "category", "gross_sales"]:
        if col in df:
            checks.append(("Missing " + col, int(df[col].isna().sum()), "Review missing values."))
    if "quantity" in df:
        checks.append(("Zero/negative quantity", int((df["quantity"] <= 0).sum()), "Check return/cancellation conventions."))
    st.dataframe(pd.DataFrame(checks, columns=["Check", "Rows flagged", "Suggested review"]), use_container_width=True, hide_index=True)

st.divider()
st.caption("Portfolio demo • Synthetic data • Validate assumptions before decisions.")
