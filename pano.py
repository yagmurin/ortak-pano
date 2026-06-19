import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from datetime import datetime, timedelta, timezone
import time
import requests
import json

# Sayfa Ayarları
st.set_page_config(page_title="Bizim Ortak Pano", page_icon="🎨", layout="centered")

# --- TÜRKİYE SAAT AYARI ---
utc_zamani = datetime.now(timezone.utc)
tr_zamani = utc_zamani + timedelta(hours=3)
su_anki_saat = tr_zamani.strftime('%H:%M')

# --- ŞIK VE MODERN TEMİZ ARAYÜZ (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3, p, label { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; color: #ffffff !important; }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff4b4b, #ff7676);
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 25px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 15px !important;
        border: 2px solid #31333f !important;
        background-color: #1a1c24 !important;
        color: white !important;
    }
    
    .stCanvas {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        margin: 0 auto !important;
    }
    
    .welcome-text {
        background-color: #1a1c24;
        padding: 10px 20px;
        border-radius: 15px;
        border: 1px solid #31333f;
        margin-bottom: 20px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎨 Ortak Duvarımız")
st.write(f"⏰ Türkiye Saati: **{su_anki_saat}**")

# --- GOOGLE SHEETS BAĞLANTI AYARI ---
SHEET_ID = "1H_Qg7vx0g7AFUf1qt8e1evzKwVaSu-QKZel9gaqqWk0"
tarih_damgasi = int(time.time())
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&t=" + str(tarih_damgasi)

def verileri_yukle_canli():
    try:
        df = pd.read_csv(SHEET_URL, header=None, skiprows=1)
        return df
    except:
        return pd.DataFrame()

notlar_df = verileri_yukle_canli()

# =========================================================
# 1. BÖLÜM: EN YENİ ATILAN MESAJLAR (SAYFANIN ÜSTÜNDE)
# =========================================================
st.subheader("💬 Duvardaki Son Notlar")

if not notlar_df.empty:
    ters_df = notlar_df.iloc[::-1]
    for index, row in ters_df.iterrows():
        try:
            v_isim = str(row.iloc[0])
            v_not = str(row.iloc[1])
            v_saat = str(row.iloc[2]) if len(row) > 2 else su_anki_saat
            v_gorsel = str(row.iloc[3]).strip() if len(row) > 3 else ""
            
            if v_isim.strip() == "" or v_not.strip() == "" or v_isim == "nan" or v_not == "nan":
                continue
                
            gors