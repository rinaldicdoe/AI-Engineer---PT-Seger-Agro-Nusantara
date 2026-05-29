PROMPT_VERSION = "weekly_sales_v1"


def build_report_prompt(summary, by_channel, by_sku, growth_table, alert_df, start_date, end_date):
    alert_md = alert_df.to_markdown(index=False) if not alert_df.empty else "Tidak ada alert."
    return f"""
Anda adalah Senior BI Analyst untuk manajemen perusahaan.
Buat laporan performa penjualan periode {start_date} sampai {end_date}.

SUMMARY KPI:
{summary.to_markdown(index=False)}

KPI BY CHANNEL:
{by_channel.to_markdown(index=False)}

KPI BY SKU:
{by_sku.head(10).to_markdown(index=False)}

GROWTH VS PREVIOUS PERIOD BY CHANNEL:
{growth_table.to_markdown(index=False)}

ANOMALY LIST:
{alert_md}

Output Markdown wajib:
# Weekly Sales Report
## Executive Summary
## KPI Highlights
## Key Insights
## Risks / Assumptions
## Recommended Actions

Rules:
- Jangan mengarang angka di luar tabel.
- Jika menyebut hipotesis, pisahkan dari fakta data.
- Gunakan bahasa Indonesia profesional, ringkas, dan action-oriented.
- Rekomendasi harus spesifik dan dapat dilakukan minggu ini.
""".strip()
