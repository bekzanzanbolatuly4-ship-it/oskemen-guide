import streamlit as st
import pandas as pd
from groq import Groq

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛЬ ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stButton>button { border-radius: 8px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- ДАННЫЕ ДЛЯ КАРТЫ (Главные точки ВКО) ---
locations = pd.DataFrame({
    'name': ['Усть-Каменогорск', 'Бухтарма', 'Катон-Карагай', 'Рахмановские ключи', 'Сибинские озера', 'Киин-Кериш'],
    'lat': [49.9487, 49.6100, 49.1725, 49.2500, 49.4444, 48.1389],
    'lon': [82.6285, 83.5100, 85.5136, 86.5000, 82.6333, 84.8111]
})

# --- ПРОВЕРКА КЛЮЧА ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔑 GROQ_API_KEY missing!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("🗺️ Путеводитель")
    st.info("🚀 **Developed by Bekzhan & DreamTeam**")
    
    st.subheader("📍 Быстрые маршруты")
    route_press = None
    if st.button("🦌 Катон-Карагай"):
        route_press = "Расскажи подробно про Катон-Карагай на языке моего запроса."
    if st.button("🏜️ Киин-Кериш"):
        route_press = "Как доехать до Киин-Кериш? Опиши на моем языке."
    if st.button("❄️ Гора Белуха"):
        route_press = "Инфо про гору Белуха и как туда попасть."
    if st.button("🌊 Озеро Маркаколь"):
        route_press = "Маршрут до озера Маркаколь и его особенности."

    st.markdown("---")
    if st.button("🗑️ Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# --- ОСНОВНОЙ КОНТЕНТ ---
st.title("🏔️ OskemenGuide AI")
st.caption("✨ *by Bekzhan and DreamTeam*")

# Вывод карты
st.subheader("📍 Карта ключевых мест ВКО")
st.map(locations)

# История чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Логика ввода
user_input = st.chat_input("Спроси на любом языке / Кез келген тілде сұраңыз...")
final_prompt = user_input or route_press

if final_prompt:
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Ты — профессиональный гид по ВКО от Bekzhan & DreamTeam. "
                            "ПРАВИЛО №1: Всегда отвечай СТРОГО на том языке, на котором написан вопрос. "
                            "Если пишут на казахском — отвечай на красивом казахском. "
                            "Если на английском — на английском. "
                            "Давай точные координаты, маршруты и советы по дорогам ВКО."
                        )
                    },
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

# --- ДАННЫЕ ДЛЯ КАРТЫ (Bekzhan & DreamTeam Edition) ---
locations = pd.DataFrame({
    'name': [
        'Усть-Каменогорск (Центр)', 
        'Бухтарма (Голубой залив)', 
        'Катон-Карагай (Заповедник)', 
        'Рахмановские ключи (Курорт)', 
        'Сибинские озера (Шалкар)', 
        'Киин-Кериш (Каньоны)',
        'Гора Белуха (Пик)',
        'Озеро Маркаколь',
        'Риддер (Ивановский белок)'
    ],
    'lat': [49.9487, 49.6100, 49.1725, 49.2500, 49.4444, 48.1389, 49.8105, 48.7000, 50.3450],
    'lon': [82.6285, 83.5100, 85.5136, 86.5000, 82.6333, 84.8111, 86.5886, 85.9500, 83.5100]
})

# Отрисовка карты
st.subheader("📍 Карта туристических маршрутов ШҚО")
st.map(locations)
