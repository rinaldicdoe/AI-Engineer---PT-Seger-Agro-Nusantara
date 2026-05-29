import pandas as pd


def build_kpi_tables(df: pd.DataFrame):
    """Hitung KPI deterministic sebelum data dikirim ke AI."""
    revenue = float(df["revenue"].sum())
    cost = float(df["cost"].sum())
    qty = int(df["qty"].sum())
    gross_margin = revenue - cost
    margin_rate = gross_margin / revenue if revenue else 0
    avg_order_value = revenue / max(qty, 1)

    summary = pd.DataFrame([{
        "total_revenue": round(revenue, 0),
        "total_qty": qty,
        "gross_margin": round(gross_margin, 0),
        "margin_rate": round(margin_rate, 4),
        "avg_order_value": round(avg_order_value, 0),
        "row_count": len(df)
    }])

    by_channel = (df.groupby("channel", as_index=False)
        .agg(total_revenue=("revenue", "sum"),
             total_qty=("qty", "sum"),
             total_cost=("cost", "sum"),
             order_count=("order_id", "nunique"))
        .assign(gross_margin=lambda x: x["total_revenue"] - x["total_cost"],
                margin_rate=lambda x: (x["total_revenue"] - x["total_cost"]) / x["total_revenue"].replace(0, pd.NA))
        .sort_values("total_revenue", ascending=False)
        .round({"margin_rate": 4}))

    by_sku = (df.groupby(["sku", "product_name"], as_index=False)
        .agg(total_revenue=("revenue", "sum"), total_qty=("qty", "sum"), order_count=("order_id", "nunique"))
        .sort_values("total_revenue", ascending=False))

    return summary, by_channel, by_sku


def calculate_growth(current: pd.DataFrame, previous: pd.DataFrame) -> pd.DataFrame:
    cur = current.groupby("channel", as_index=False).agg(current_revenue=("revenue", "sum"))
    prev = previous.groupby("channel", as_index=False).agg(previous_revenue=("revenue", "sum"))
    growth = cur.merge(prev, on="channel", how="outer").fillna(0)
    growth["growth_rate"] = (growth["current_revenue"] - growth["previous_revenue"]) / growth["previous_revenue"].replace(0, 1)
    return growth.sort_values("growth_rate")
