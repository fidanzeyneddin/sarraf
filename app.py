import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Kur Çevirici / محول العملات", page_icon="💰")

# API Anahtarı
API_KEY = "14247b32cea1cc48c3465bc3"

# --- DİL SÖZLÜĞÜ ---
diller = {
    "Türkçe": {
        "baslik": "💰 Döviz Dönüştürücü",
        "miktar_etiket": "Dönüştürülecek Miktar",
        "kaynak_etiket": "Kaynak Birim",
        "hedef_etiket": "Hedef Birim",
        "buton": "Hesapla",
        "hata_api": "API hatası! Anahtarı kontrol edin.",
        "hata_baglanti": "Bağlantı hatası oluştu.",
        "sonuc_metni": "Sonuç",
        "kur_metni": "Güncel Kur",
        "direction": "ltr"
    },
    "العربية": {
        "baslik": "💰 محول العملات السريع",
        "miktar_etiket": "المبلغ المراد تحويله",
        "kaynak_etiket": "من عملة",
        "hedef_etiket": "إلى عملة",
        "buton": "تحويل الآن",
        "hata_api": "خطأ في المفتاح البرمجي",
        "hata_baglanti": "حدث خطأ في الاتصال",
        "sonuc_metni": "النتيجة",
        "kur_metni": "سعر الصرف الحالي",
        "direction": "rtl"
    }
}

# --- YAN MENÜ ---
secilen_dil_adi = st.sidebar.selectbox("Dil / اللغة", ["Türkçe", "العربية"])
dil = diller[secilen_dil_adi]

# --- DİNAMİK STİL ---
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        direction: {dil['direction']};
        text-align: {'right' if dil['direction'] == 'rtl' else 'left'};
        font-family: 'Cairo', sans-serif;
    }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; background-color: #28a745; color: white; }}
    </style>
    """, unsafe_allow_html=True)

st.title(dil["baslik"])

# Giriş Alanları
miktar = st.number_input(dil["miktar_etiket"], min_value=0.0, value=1.0)

col1, col2 = st.columns(2)
# BURAYA SYP (Suriye Lirası) EKLENDİ
para_birimleri = ["TRY", "USD", "EUR", "SYP"]

with col1:
    baz_birim = st.selectbox(dil["kaynak_etiket"], para_birimleri)
with col2:
    hedef_birim = st.selectbox(dil["hedef_etiket"], para_birimleri)

# Hesaplama
if st.button(dil["buton"]):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{baz_birim}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            kur = data['conversion_rates'][hedef_birim]
            sonuc = miktar * kur
            
            st.success(f"### {dil['sonuc_metni']}: {sonuc:.2f} {hedef_birim}")
            st.info(f"{dil['kur_metni']}: 1 {baz_birim} = {kur:.4f} {hedef_birim}")
        else:
            st.error(dil["hata_api"])
    except:
        st.error(dil["hata_baglanti"])