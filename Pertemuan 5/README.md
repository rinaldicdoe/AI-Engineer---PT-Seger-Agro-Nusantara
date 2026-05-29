# AI Auto-Report Reference Solution

Project ini adalah versi lengkap untuk trainer. Peserta dapat menulis ulang kode bertahap mengikuti slide praktik.

## Dataset yang dipakai

1. `data/orders.csv` dan tabel SQLite `orders` — data transaksi utama untuk KPI, growth, dan anomali.
2. `data/products.csv` dan tabel SQLite `products` — master produk untuk konteks SKU/kategori.
3. `data/channel_targets.csv` dan tabel SQLite `channel_targets` — target channel mingguan untuk pengembangan lanjutan.
4. `data/retail_bi.db` — database SQLite yang sudah siap dipakai.

## Setup

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env  # Windows
# atau: cp .env.example .env
```

Default `USE_MOCK_AI=true`, jadi project bisa jalan tanpa API key. Untuk memakai OpenAI API, isi `OPENAI_API_KEY` dan ubah `USE_MOCK_AI=false`.

## Jalankan report dari Python

```bash
python -c "from app.report_service import generate_report; print(generate_report('2026-05-11','2026-05-17','html'))"
```

## Jalankan API

```bash
uvicorn app.main:app --reload
```

Buka `http://127.0.0.1:8000/docs`, lalu coba endpoint `POST /generate-report` dengan:

```json
{
  "start_date": "2026-05-11",
  "end_date": "2026-05-17",
  "output_format": "pdf"
}
```

## Output

File report akan muncul di:

- `outputs/markdown/`
- `outputs/html/`
- `outputs/pdf/` jika WeasyPrint berhasil
- `outputs/logs/`

Jika PDF gagal karena dependency OS WeasyPrint, gunakan output HTML sebagai hasil final sementara.
