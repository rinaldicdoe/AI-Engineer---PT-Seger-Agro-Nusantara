import pandas as pd
from sqlalchemy import create_engine, text

REQUIRED_COLUMNS = ["order_date", "channel", "sku", "qty", "revenue", "cost", "status"]

def pull_sales_data(database_url: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Ambil order completed/returned pada periode terpilih."""
    engine = create_engine(database_url)
    query = text("""
        SELECT order_id, order_date, channel, region, sku, product_name, category,
               qty, unit_price, discount_amount, revenue, cost, status
        FROM orders
        WHERE order_date BETWEEN :start_date AND :end_date
        ORDER BY order_date, channel, sku
    """)
    df = pd.read_sql(query, engine, params={"start_date": start_date, "end_date": end_date})
    if df.empty:
        raise ValueError(f"Data kosong untuk periode {start_date} sampai {end_date}")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}")
    return df
