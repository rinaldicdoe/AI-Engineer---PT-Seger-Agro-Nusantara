import streamlit as st

st.title("Latihan 01 - Streamlit Dasar")
st.write("Halo, ini aplikasi Streamlit pertama saya.")

nama = st.text_input("Nama Anda")

if nama:
  st.success(f"Selamat belajar, {nama}!")
