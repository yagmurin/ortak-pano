import streamlit as st
import datetime
from streamlit_drawable_canvas import st_canvas

# Sayfa genişliğini ayarlayalım ki çizim alanı rahat sığsın
st.set_page_config(layout="wide")

st.title("📌 Ortak Not ve Çizim Panosu")
st.write("Bu panoya gruptaki herkes yazı yazabilir veya el yazısı/çizim bırakabilir.")

# Hafızayı başlatalım (Yazılar ve Çizimler için)
if "pano_icerikleri" not in st.session_state:
    st.session_state.pano_icerikleri = []

# Sol tarafta giriş alanları olsun
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("✍️ Yeni Bir Şey Ekle")
    
    # Herkes kendi adını özgürce yazabilir
    isim = st.text_input("İsminiz nedir?", placeholder="Buraya adınızı yazın...")
    
    # Giriş türü seçimi
    tur = st.radio("Ne eklemek istersin?", ["Normal Yazı", "El Çizimi / El Yazısı"])
    
    yeni_not = ""
    cizim_verisi = None
    
    if tur == "Normal Yazı":
        yeni_not = st.text_area("Notunu buraya yaz...")
    else:
        st.write("🎨 Çizim Ayarları:")
        secilen_renk = st.color_picker("Çizim Rengini Seç:", "#1f77b4")
        kalinlik = st.slider("Fırça Kalınlığı:", min_value=1, max_value=20, value=3)
        
        st.write("Aşağıdaki kutuya farenle veya dokunmatik ekranla çizim/yazı bırak:")
        
        cizim_verisi = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=kalinlik,
            stroke_color=secilen_renk,
            background_color="#eee",
            height=250,
            key="canvas",
        )

    if st.button("Panoya Gönder"):
        if isim.strip() == "":
            st.error("Lütfen önce isminizi yazın!")
        else:
            zaman = datetime.datetime.now().strftime("%H:%M")
            
            if tur == "Normal Yazı" and yeni_not.strip() != "":
                st.session_state.pano_icerikleri.insert(0, {"tip": "metin", "isim": isim, "zaman": zaman, "icerik": yeni_not})
                st.success("Notun panoya eklendi!")
            elif tur == "El Çizimi / El Yazısı" and cizim_verisi is not None and cizim_verisi.image_data is not None:
                st.session_state.pano_icerikleri.insert(0, {"tip": "cizim", "isim": isim, "zaman": zaman, "icerik": cizim_verisi.image_data})
                st.success("Çizimin panoya eklendi!")
            else:
                st.error("Lütfen boş bırakma!")

# Sağ tarafta pano sergilensin
with col2:
    st.subheader("📋 Duvardaki Pano")
    if not st.session_state.pano_icerikleri:
        st.info("Pano henüz boş. İlk izi sen bırak!")
    else:
        for oge in st.session_state.pano_icerikleri:
            with st.container(border=True):
                st.write(f"👤 **{oge['isim']}** | 🕒 {oge['zaman']}")
                if oge["tip"] == "metin":
                    st.info(oge["icerik"])
                elif oge["tip"] == "cizim":
                    st.image(oge["icerik"], caption=f"{oge['isim']} tarafından çizildi", width=300)