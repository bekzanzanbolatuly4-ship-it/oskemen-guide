import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- SEO ЖӘНЕ ПАРАМЕТРЛЕР ---
st.set_page_config(page_title="OskemenGuide SuperApp", page_icon="🧭", layout="wide")

# Google Verification (Алдыңғы кодтан қалдырамыз)
st.markdown('<meta name="google-site-verification" content="google7a49481bcf67fe79" />', unsafe_allow_html=True)

# --- SIDEBAR НАВИГАЦИЯ ---
with st.sidebar:
    st.title("🏔️ Oskemen SuperApp")
    st.write("v1.5.0 | **DreamTeam**")
    
    # МӘЗІР (ВКЛАДКАЛАР)
    menu = st.radio("Бөлімді таңдаңыз:", 
                    ["📍 Навигатор", "🏨 Қонақ үйлер", "🚐 Турлар", "🎭 Ойын-сауық", "🤖 AI Көмекші"])
    
    st.markdown("---")
    st.subheader("💚 Қолдау (Donate)")
    try:
        st.image("donate.jpg", use_container_width=True)
    except:
        st.caption("Halyk QR: donate.jpg")

# --- 1. НАВИГАТОР БӨЛІМІ ---
if menu == "📍 Навигатор":
    st.header("📍 ШҚО Табиғаты мен Навигация")
    # (Мұнда баяғы карта мен жерлер тізімі тұрады)
    destinations = {
        "🦌 Катон-Карагай": {"lat": 49.1725, "lon": 85.5136, "desc": "Алтай маржаны."},
        "🏖️ Бухтарма": {"lat": 49.6100, "lon": 83.5100, "desc": "Жазғы демалыс."},
        "🧱 Киин-Кериш": {"lat": 48.1389, "lon": 84.8111, "desc": "Марс пейзажы."}
    }
    sel_place = st.selectbox("Қайда барамыз?", list(destinations.keys()))
    st.map(pd.DataFrame([destinations[sel_place]]))
    st.info(destinations[sel_place]["desc"])

# --- 2. ҚОНАҚ ҮЙЛЕР БӨЛІМІ ---
elif menu == "🏨 Қонақ үйлер":
    st.header("🏨 Демалыс орындары мен Қонақ үйлер")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Өскемен қаласы")
        st.write("- **Shiny River** (Ертіс жағалауы)")
        st.write("- **Best Western Plus**")
        st.button("Booking-тен қарау", key="btn1")
        
    with col2:
        st.subheader("Таулы аймақтар")
        st.write("- **Рахман қайнарлары** (Шыпажай)")
        st.write("- **Алтай Resort** (Катон)")
        st.button("Брондау (2GIS)", key="btn2")

# --- 3. ТУРЛАР БӨЛІМІ ---
elif menu == "🚐 Турлар":
    st.header("🚐 Дайын туристік турлар")
    st.success("🔥 Тренд: 3 күндік Катон-Карагай туры - 85,000 ₸")
    st.write("1. **Джип-тур:** Киин-Кериш пен Шекельмес.")
    st.write("2. **Экспедиция:** Мұзтау етегіне жорық.")
    st.write("3. **Фото-тур:** Алтайдың ең әдемі жерлері.")
    st.text_input("Турға жазылу (Телефон нөміріңіз):")

# --- 4. ОЙЫН-САУЫҚ БӨЛІМІ ---
elif menu == "🎭 Ойын-сауық":
    st.header("🎭 Қайда баруға болады?")
    tab1, tab2, tab3 = st.tabs(["⛷️ Спорт", "🍽️ Ресторандар", "🏛️ Мәдениет"])
    
    with tab1:
        st.write("🎿 **Алтай Альпілері** - тау шаңғысы.")
        st.write("🎿 **Нұртау** - отбасылық демалыс.")
    with tab2:
        st.write("🥩 **Two Bulls** - стейк-хаус.")
        st.write("☕ **Coffee Like** - ең дәмді кофе.")
    with tab3:
        st.write("🎭 **Жамбыл атындағы театр**.")
        st.write("🏛️ **Этно-парк** - ашық аспан астындағы музей.")

# --- 5. AI КӨМЕКШІ БӨЛІМІ ---
elif menu == "🤖 AI Көмекші":
    st.header("🤖 Смарт Консультант")
    st.write("Менен турлар, отельдер немесе ШҚО тарихы туралы сұраңыз!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Сұрақ қойыңыз..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Сен ШҚО бойынша SuperApp гидісің. Отельдер, турлар және ойын-сауық туралы ақпарат бересің."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                ).choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API Error")
