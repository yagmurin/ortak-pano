import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import pytz
import time

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
            v_isim = str(row.iloc[1]) if len(row) > 1 else str(row.iloc[0])
            v_not = str(row.iloc[2]) if len(row) > 2 else str(row.iloc[1])
            v_gorsel = str(row.iloc[3]).strip() if len(row) > 3 else ""
            v_saat = str(row.iloc[0]).split(" ")[1][:5] if (" " in str(row.iloc[0])) else su_anki_saat
            
            if v_isim.strip() == "" or v_not.strip() == "" or v_isim == "nan" or v_not == "nan":
                continue
                
            gorsel_html = ""
            if v_gorsel != "" and v_gorsel != "nan" and (v_gorsel.startswith("http") or v_gorsel.startswith("www")):
                gorsel_html = f'<img src="{v_gorsel}" style="max-width: 100%; border-radius: 12px; margin-top: 12px; display: block; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">'

            st.markdown(f"""
            <div style="background-color: #1a1c24; padding: 18px; border-radius: 18px; margin-bottom: 12px; border-left: 6px solid #ff4b4b; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <span style="color: #ff4b4b; font-weight: bold; font-size: 16px;">{v_isim}</span> 
                <span style="color: #888; font-size: 12px; float: right;">🕒 {v_saat}</span>
                <p style="margin-top: 8px; margin-bottom: 0; color: #e0e0e0 !important; font-size: 15px;">{v_not}</p>
                {gorsel_html}
            </div>
            """, unsafe_allow_html=True)
        except:
            continue
else:
    st.write("Şu an duvar boş görünüyor. İlk kalıcı notu aşağıdan sen uçur!")

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
    
    st.write("📌 Duvara Ömür Boyu Kalıcı Not Bırak")
    st.caption("Mesajınıza fotoğraf veya GIF eklemek istiyorsanız, internetteki herhangi bir görselin üzerine sağ tıklayıp 'Resim adresini kopyala' deyin ve alttaki ilgili kutuya yapıştırın!")
    
    GOOGLE_FORM_LINKI = "https://docs.google.com/forms/d/e/1FAIpQLScC1L8Z_AIsJb0uB0BwOnd08pY7BqI0Sre5gMWhbXzZ_K6w9A/viewform?embedded=true"
    st.markdown(f'<iframe src="{GOOGLE_FORM_LINKI}" width="100%" height="450" frameborder="0" marginheight="0" marginwidth="0">Yükleniyor…</iframe>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- AÇILIR KAPANIR KORUNAKLI ÇİZİM ALANI ---
    with st.expander("🎨 Çizim Yapmak İçin Tıkla"):
        st.write("Buraya dilediğiniz gibi çizim yapabilirsiniz. İşiniz bittiğinde yukarıdaki başlığa tekrar basarak kapatabilirsiniz:")
        
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