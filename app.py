import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="محول العملات", page_icon="💰")

# Arapça için sağdan sola (RTL) metin desteği ve stil ayarları
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 محول العملات السريع")
st.write("حول أموالك بين الليرة التركية، الدولار، واليورو بأسعار حقيقية.")

# API Anahtarı (Buraya kendi anahtarını yapıştır)
API_KEY = "14247b32cea1cc48c3465bc3"

# Seçenekler Sözlüğü (Kod tarafında işlem yapmak, kullanıcıya Arapça göstermek için)
birimler = {
    "الليرة التركية (TRY)": "TRY",
    "الدولار الأمريكي (USD)": "USD",
    "اليورو (EUR)": "EUR"
}

# Kullanıcı Giriş Alanları
miktar = st.number_input("المبلغ المراد تحويله", min_value=0.0, value=1.0, step=1.0)

col1, col2 = st.columns(2)

with col1:
    kaynak_secim = st.selectbox("من عملة", list(birimler.keys()))

with col2:
    hedef_secim = st.selectbox("إلى عملة", list(birimler.keys()))

baz_birim = birimler[kaynak_secim]
hedef_birim = birimler[hedef_secim]

# Hesaplama Butonu
if st.button("تحويل الآن"):
    with st.spinner('جاري جلب البيانات...'):
        try:
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{baz_birim}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                kur = data['conversion_rates'][hedef_birim]
                sonuc = miktar * kur
                
                st.balloons()
                st.success(f"### النتيجة: {sonuc:.2f} {hedef_birim}")
                st.info(f"سعر الصرف الحالي: 1 {baz_birim} = {kur:.4f} {hedef_birim}")
            else:
                st.error("خطأ في المفتاح البرمجي (API Key). يرجى التأكد منه.")
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")

st.markdown("---")
st.caption("يتم تحديث الأسعار تلقائياً عبر ExchangeRate-API")