import os
from app.config import OPENAI_MODEL, USE_MOCK_AI

REQUIRED_SECTIONS = [
    "Executive Summary",
    "KPI Highlights",
    "Key Insights",
    "Risks / Assumptions",
    "Recommended Actions"
]

def validate_report_sections(report_md):
    missing = [s for s in REQUIRED_SECTIONS if s not in report_md]
    if missing:
        raise ValueError(f"Section wajib hilang: {missing}")
    return report_md


def _mock_narrative(prompt: str) -> str:
    return """# Weekly Sales Report

## Executive Summary
Revenue periode ini sudah dihitung dari data transaksi dan diringkas dalam tabel KPI. Perubahan terbesar perlu dilihat pada channel dengan growth negatif karena berpotensi memengaruhi target mingguan. Prioritas minggu ini adalah mengecek channel yang turun, menjaga stok SKU teratas, dan memastikan promo tidak menekan margin secara berlebihan.

## KPI Highlights
- Total revenue, quantity, gross margin, dan AOV tersedia pada tabel summary pipeline.
- Channel dengan kontribusi terbesar perlu dijaga melalui stok dan campaign yang konsisten.
- SKU dengan revenue tertinggi dapat diprioritaskan untuk bundle dan optimasi traffic.

## Key Insights
1. Perubahan performa antar-channel menunjukkan area yang perlu divalidasi bersama tim sales dan marketing.
2. Growth negatif perlu dicek terhadap stok, diskon, retur, traffic, dan perubahan campaign.
3. Produk dengan qty tinggi tetapi margin rendah perlu dipantau agar tidak menggerus profit.

## Risks / Assumptions
- Narasi mock digunakan karena USE_MOCK_AI=true atau API key belum tersedia.
- Semua angka mengikuti output KPI dari Pandas/SQL, bukan dihitung ulang oleh AI.
- Penyebab bisnis masih berupa hipotesis dan perlu validasi dengan tim terkait.

## Recommended Actions
1. Review channel dengan penurunan terbesar dan cek campaign aktif pada periode tersebut.
2. Pastikan SKU top revenue memiliki stok cukup untuk satu minggu ke depan.
3. Validasi diskon dan retur agar margin tetap sehat.
"""


def generate_ai_narrative(prompt: str) -> str:
    if USE_MOCK_AI or not os.getenv("OPENAI_API_KEY"):
        report_md = _mock_narrative(prompt)
    else:
        from openai import OpenAI
        client = OpenAI()
        response = client.responses.create(model=OPENAI_MODEL, input=prompt)
        report_md = response.output_text

    missing = [section for section in REQUIRED_SECTIONS if section not in report_md]
    if missing:
        raise ValueError(f"Section wajib hilang dari output AI: {missing}")
    return report_md
