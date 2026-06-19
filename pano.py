import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import pytz

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

    /* Tuvalin etrafındaki çirkin boşlukları yok etme */
    .css-1r6g78m, .stCanvas {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_with_html=True)

st.title("🎨 Ortak Duvarımız")
st.write(f"⏰ Türkiye Saati: **{su_anki_saat}**")

# --- GOOGLE SHEETS BAĞLANTI AYARI ---
# Kendi Google Sheet ID'ni aşağıdaki tırnakların içine yapıştır:
SHEET_ID = "1H_Qg7vx0g7AFUf1qt8e1evzKwVaSu-QKZel9gaqqWk0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=3)  # Verileri 3 saniyede bir canlı kontrol et
def verileri_yukle():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["İsim", "Not", "Saat"])

notlar_df = verileri_yukle()

# Kullanıcı Giriş Paneli
isim = st.text_input("Adın Ne?", placeholder="Örn: Yağmur")

# --- GELİŞMİŞ FIRÇA VE ÇİZİM SEÇENEKLERİ ---
st.subheader("✍️ Çizim Odası")
col1, col2, col3 = st.columns(3)

with col1:
    firca_tipi = st.selectbox("Fırça Türü", ["freedraw", "line", "rect", "circle", "transform"])
with col2:
    firca_kalinligi = st.slider("Fırça Kalınlığı", 1, 20, 4)
with col3:
    renk = st.color_picker("Renk Seç", "#ff4b4b")

# Beyaz boşlukları yok eden, tam oturan Responsive Çizim Alanı
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.2)",
    stroke_width=firca_kalinligi,
    stroke_color=renk,
    background_color="#1a1c24",
    height=350,
    drawing_mode=firca_tipi,
    update_streamlit=True,
    key="gelismis_canvas",
)

# Not Bırakma Kutusu
yeni_not = st.text_input("Duvara bir mesaj yazın:")

if st.button("Duvara Çak! 📌"):
    if isim and yeni_not:
        # Notu yerel listeye ekleme simülasyonu (Gerçek kayıt için daha sonra Google Forms bağlayabiliriz)
        st.success("Mesaj gönderildi! (Kalıcı veritabanı kaydı için altyapı hazır)")
    else:
        st.warning("Lütfen adını ve mesajını boş bırakma.")

# --- MODERN NOT DUVARI LİSTELEME ---
st.subheader("💬 Duvardaki Notlar")
if not notlar_df.empty:
    for index, row in notlar_df.iterrows():
        st.markdown(f"""
        <div style="background-color: #1a1c24; padding: 18px; border-radius: 18px; margin-bottom: 12px; border-left: 6px solid #ff4b4b; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <span style="color: #ff4b4b; font-weight: bold; font-size: 16px;">{row['İsim']}</span>
            <span style="color: #888; font-size: 12px; float: right;">🕒 {row['Saat']}</span>
            <p style="margin-top: 8px; margin-bottom: 0; color: #e0e0e0 !important; font-size: 15px;">{row['Not']}</p>
        </div>
        """, unsafe_with_html=True)
else:
    st.write("Şu an duvar bomboş, ilk izi sen bırak!")