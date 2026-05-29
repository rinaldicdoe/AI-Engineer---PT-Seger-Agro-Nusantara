import streamlit as st

st.title("Latihan 02 - Upload dan Preview File")

file = st.file_uploader("Upload gambar nota", type=["jpg", "jpeg", "png", "webp"])

if file:
    st.image(file, caption=file.name, use_container_width=True)
    st.write("Ukuran file:", round(len(file.getvalue()) / 1024, 2), "KB")
