from pathlib import Path
import pandas as pd

def test_sample_dataset_has_expected_columns():
    path = Path(__file__).parents[1] / "data" / "sample_ecommerce_orders.csv"
    df = pd.read_csv(path)
    expected = {"order_id", "order_date", "gross_sales", "net_revenue", "order_status", "category"}
    assert expected.issubset(df.columns)
    assert len(df) >= 100
