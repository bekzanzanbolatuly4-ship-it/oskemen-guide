import streamlit as st
from groq import Groq

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛЬ И ДИЗАЙН ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        border: 1px solid #d1d5db;
        transition: all 0.3s;
    }
    .stButton>button:hover { border-color: #007bff; color: #007bff; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- ПРОВЕРКА API КЛЮЧА ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔑 GROQ_API_KEY missing in Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ (КОМАНДА И МАРШРУТЫ) ---
with st.sidebar:
    st.title("🗺️ Навигация")
    
    st.subheader("📍 Готовые маршруты")
    route_press = None
    
    if st.button("🦌 Катон-Карагай (Заповедник)"):
        route_press = "Опиши подробный маршрут в Катон-Карагай: что посмотреть, где остановиться и как доехать."
    
    if st.button("🧱 Киин-Кериш (Пылающие скалы)"):
        route_press = "Как добраться до Киин-Кериша? Что нужно знать о дороге и какую машину выбрать?"
    
    if st.button("🌲 Рахмановские ключи"):
        route_press = "Расскажи о поездке на Рахмановские ключи: маршрут и лечебные свойства."
    
    if st.button("🏖️ Бухтарма & Сибины"):
        route_press = "Сравни отдых на Бухтарме и Сибинских озерах. Куда лучше поехать?"

    st.markdown("---")
    st.subheader("👥 Наша Команда")
    st.info("🚀 **Developed by Bekzhan**\n\n**& DreamTeam**")
    
    if st.button("🗑️ Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# --- ОСНОВНОЙ БЛОК ---
st.title("🏔️ OskemenGuide AI")
st.markdown("#### Твой цифровой проводник по Восточному Казахстану")
st.caption("✨ *Created by Bekzhan and DreamTeam*")

# Вывод истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Логика ввода
user_input = st.chat_input("Напишите вопрос (на любом языке)...")
final_prompt = user_input or route_press

if final_prompt:
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Используем топовую модель для лучшего казахского и русского
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Ты — главный ИИ-гид по Восточно-Казахстанской области. "
                            "Твои создатели — Bekzhan и DreamTeam. "
                            "Твоя задача: давать точные, интересные и полезные маршруты. "
                            "Понимай любые опечатки. Отвечай строго на языке пользователя. "
                            "Если спрашивают на казахском — используй красивый литературный язык."
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
            st.error(f"Ошибка: {e}")

