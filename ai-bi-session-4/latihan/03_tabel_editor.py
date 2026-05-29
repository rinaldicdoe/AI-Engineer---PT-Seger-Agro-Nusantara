import streamlit as st
import pandas as pd

st.title("Latihan 03 - Tabel Editable")

data = pd.DataFrame([
    {"nama_barang": "Kopi", "qty": 2, "harga_satuan": 12000, "total_harga": 24000},
    {"nama_barang": "Roti", "qty": 1, "harga_satuan": 8000, "total_harga": 8000},
])

edited = st.data_editor(data, num_rows="dynamic", use_container_width=True)

edited["total_harga"] = edited["qty"] * edited["harga_satuan"]
st.session_state["edited"] = edited

st.metric("Grand Total", f"Rp {edited['total_harga'].sum():,.0f}")
