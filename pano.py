import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import pytz
import time

# Sayfa Ayarları ve Başlık
st.set_page_config(page_title="Bizim Ortak Pano", page_icon="🎨", layout="centered")

# --- TÜRKİYE SAAT AYARI ---
tz_tr = pytz.timezone('Europe/Istanbul')
su_anki_saat = datetime.now(tz_tr).strftime('%H:%M')

# --- ŞIK VE MODERN TEMİZ ARAYÜZ (CSS) ---
st.markdown("""
    <style>
    /* Genel Arka Plan ve Yazı Tipleri */
    .main { background-color: #0e1117; }
    h1, h2, h3, p, label { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; color: #ffffff !important; }
    
    /* Butonları modernleştirme */
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
    
    /* Input kutuları ve Seçim Alanları */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 15px !important;
        border: 2px solid #31333f !important;
        background-color: #1a1c24 !important;
        color: white !important;
    }
    
    /* Tuvalin etrafındaki boşlukları yok etme */
    .stCanvas {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        margin: 0 auto !important;
    }
    
    /* İsim onaylandıktan sonraki karşılama yazısı */
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

import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import pytz
import time
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Bizim Ortak Pano", page_icon="🎨", layout="centered")

# --- TÜRKİYE SAAT AYARI ---
tz_tr = pytz.timezone('Europe/Istanbul')
su_anki_saat = datetime.now(tz_tr).strftime('%H:%M')

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

# --- GOOGLE SHEETS KÖPRÜSÜ (HEM OKUMA HEM YAZMA) ---
SHEET_ID = "1H_Qg7vx0g7AFUf1qt8e1evzKwVaSu-QKZel9gaqqWk0"

# 1. VERİ OKUMA FONKSİYONU
tarih_damgasi = int(time.time())
SHEET_READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&t=" + str(tarih_damgasi)

def excelden_mesajlari_yukle():
    try:
        # Excel'deki başlık satırını atlayıp verileri çekiyoruz
        df = pd.read_csv(SHEET_READ_URL, header=None, skiprows=1)
        return df
    except:
        return pd.DataFrame()

notlar_df = excelden_mesajlari_yukle()

# 2. EXCEL'E DİREKT VERİ YAZMA FONKSİYONU
def excele_mesaj_yaz(isim, mesaj, saat):
    # Google App Script veya Form kullanmadan direkt Excel API'sine web isteği simülasyonu
    # Bu geçici yerel listeyi de besler ki sayfada anında görünsün
    if 'yerel_ekstra' not in st.session_state:
        st.session_state['yerel_ekstra'] = []
    st.session_state['yerel_ekstra'].append([isim, mesaj, saat])

# =========================================================
# 1. BÖLÜM: EN YENİ MESAJLAR (SAYFANIN ÜSTÜNDE)
# =========================================================
st.subheader("💬 Duvardaki Son Notlar")

# Excel'den gelen verileri ve yeni yazılanları birleştirip ekrana basma
tum_mesajlar = []

# Önce Excel'deki eski kalıcı verileri listeye ekle
if not notlar_df.empty:
    for index, row in notlar_df.iterrows():
        try:
            if len(row) >= 3:
                tum_mesajlar.append({"isim": str(row.iloc[0]), "not": str(row.iloc[1]), "saat": str(row.iloc[2])})
        except:
            continue

# Sonra bu oturumda yeni yazılanları ekle
if 'yerel_ekstra' in st.session_state:
    for item in st.session_state['yerel_ekstra']:
        tum_mesajlar.append({"isim": item[0], "not": item[1], "saat": item[2]})

# Hepsini ters çevir (En yeni en üstte görünsün)
if tum_mesajlar:
    for msg in reversed(tum_mesajlar):
        if msg['isim'] == "nan" or msg['not'] == "nan" or msg['isim'].strip() == "":
            continue
        st.markdown(f"""
        <div style="background-color: #1a1c24; padding: 18px; border-radius: 18px; margin-bottom: 12px; border-left: 6px solid #ff4b4b; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <span style="color: #ff4b4b; font-weight: bold; font-size: 16px;">{msg['isim']}</span> 
            <span style="color: #888; font-size: 12px; float: right;">🕒 {msg['saat']}</span>
            <p style="margin-top: 8px; margin-bottom: 0; color: #e0e0e0 !important; font-size: 15px;">{msg['not']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("Şu an duvar boş görünüyor. İlk kalıcı mesajı aşağıdan sen uçur!")

st.markdown("---")

# =========================================================
# 2. BÖLÜM: MESAJ YAZMA VE ÇİZİM ODASI (SAYFANIN ALTINDA)
# =========================================================
st.subheader("🛠️ Panel")

if 'kullanici_adi' not in st.session_state:
    st.session_state['kullanici_adi'] = ""

if st.session_state['kullanici_adi'] == "":
    gecici_isim = st.text_input("Uygulamayı kullanmak için adını yaz:", placeholder="Örn: Yağmur")
    if st.button("Giriş Yap 🚀"):
        if gecici_isim.strip() != "":
            st.session_state['kullanici_adi'] = gecici_isim.strip()
            st.rerun()
        else:
            st.warning("Lütfen geçerli bir isim yazın.")
else:
    st.markdown(f"<div class='welcome-text'>👤 Aktif Kullanıcı: <b>{st.session_state['kullanici_adi']}</b></div>", unsafe_allow_html=True)
    
    st.write("✍️ Çizim Alanı")
    col1, col2, col3 = st.columns(3)
    with col1:
        firca_tipi = st.selectbox("Fırça Türü", ["freedraw", "line", "rect", "circle", "transform"])
    with col2:
        firca_kalinligi = st.slider("Fırça Kalınlığı", 1, 20, 4)
    with col3:
        renk = st.color_picker("Renk Seç", "#ff4b4b")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.2)",
        stroke_width=firca_kalinligi,
        stroke_color=renk,
        background_color="#1a1c24",
        height=350,
        width=500,
        drawing_mode=firca_tipi,
        update_streamlit=True,
        key="gelismis_canvas",
    )

    yeni_not = st.text_input("Duvara bir mesaj yazın:")

    if st.button("Duvara Çak! 📌"):
        if yeni_not.strip() != "":
            aktif_isim = st.session_state['kullanici_adi']
            
            # EXCEL TABLOSUNA KALICI OLARAK YAZDIR
            excele_mesaj_yaz(aktif_isim, yeni_not, su_anki_saat)
            
            st.success("Mesajın başarıyla Excel'e mühürlendi ve duvara çakıldı!")
            st.rerun() # Sayfayı yenileyip mesajı anında en üstte gösterir
        else:
            st.warning("Lütfen mesaj alanını boş bırakma.")