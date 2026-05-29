import pandas as pd


def detect_anomalies(growth_table: pd.DataFrame, threshold: float = -0.20) -> pd.DataFrame:
    alerts = []
    for _, row in growth_table.iterrows():
        if row["growth_rate"] < threshold:
            alerts.append({
                "metric": "revenue_growth",
                "dimension": row["channel"],
                "severity": "high" if row["growth_rate"] < -0.30 else "medium",
                "message": f"Revenue channel {row['channel']} turun {row['growth_rate']:.1%} vs periode sebelumnya",
                "recommended_check": "Cek campaign, diskon, stok, retur, dan perubahan traffic channel."
            })
    return pd.DataFrame(alerts)


def build_alert_message(alert_df: pd.DataFrame, report_path: str) -> str:
    if alert_df.empty:
        return "Tidak ada alert prioritas pada periode ini."
    lines = ["[AUTO-REPORT ALERT]"]
    for _, row in alert_df.iterrows():
        lines.append(f"- {row['severity'].upper()} | {row['message']}")
        lines.append(f"  Cek: {row['recommended_check']}")
    lines.append(f"Report lengkap: {report_path}")
    return "\n".join(lines)
