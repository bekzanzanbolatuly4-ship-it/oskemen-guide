import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛЬ ---
st.markdown("""<style>.stChatMessage { border-radius: 15px; } .stButton>button { width: 100%; border-radius: 8px; }</style>""", unsafe_allow_html=True)

# --- ГЕОЛОКАЦИЯ ---
loc = get_geolocation() 
user_lat, user_lon = None, None
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']

# --- ПОЛНЫЙ СПИСОК МЕСТ ВКО ---
destinations = {
    "🦌 Катон-Карагай": {"lat": 49.1725, "lon": 85.5136},
    "💦 Рахмановские ключи": {"lat": 49.2500, "lon": 86.5000},
    "🏖️ Бухтарма (Голубой залив)": {"lat": 49.6100, "lon": 83.5100},
    "💎 Сибинские озёра": {"lat": 49.4444, "lon": 82.6333},
    "🧱 Киин-Кериш": {"lat": 48.1389, "lon": 84.8111},
    "🏔️ Гора Белуха": {"lat": 49.8105, "lon": 86.5886},
    "🐟 Озеро Маркаколь": {"lat": 48.7000, "lon": 85.9500},
    "⛷️ Риддер (Ивановский белок)": {"lat": 50.3450, "lon": 83.5100},
    "🌊 Озеро Зайсан": {"lat": 48.0000, "lon": 84.0000},
    "🏛️ Монастырские озёра": {"lat": 49.3800, "lon": 82.5500},
    "🏜️ Шекельмес": {"lat": 48.0500, "lon": 84.5000},
    "🌲 Западно-Алтайский заповедник": {"lat": 50.3000, "lon": 83.8000}
}

# --- ПРОВЕРКА КЛЮЧА ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.title("🧭 Навигатор ВКО")
    st.info("🚀 **Bekzhan & DreamTeam**")
    
    if user_lat:
        st.success("✅ Ваша локация определена")
    else:
        st.warning("⚠️ Локация не определена. Маршруты будут из Усть-Каменогорска.")

    st.subheader("🏁 Выберите пункт назначения:")
    selected_route = None
    for place in destinations:
        if st.button(place):
            origin = f"моих координат ({user_lat}, {user_lon})" if user_lat else "Усть-Каменогорска"
            selected_route = f"Построй подробный маршрут от {origin} до {place}. Укажи время в пути, состояние дороги и важные советы."

    st.markdown("---")
    if st.button("🗑️ Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# --- ОСНОВНОЙ КОНТЕНТ ---
st.title("🏔️ OskemenGuide AI")
st.caption("✨ by Bekzhan & DreamTeam — Все дороги Восточного Казахстана")

# Отрисовка большой карты
map_list = []
for name, coords in destinations.items():
    map_list.append({'lat': coords['lat'], 'lon': coords['lon'], 'name': name})
if user_lat:
    map_list.append({'lat': user_lat, 'lon': user_lon, 'name': 'ВЫ ЗДЕСЬ'})

st.map(pd.DataFrame(map_list))

# Отображение чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Логика ввода
prompt = st.chat_input("Напишите место или вопрос...")
final_prompt = prompt or selected_route

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"): st.markdown(final_prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "Ты экспертный гид-навигатор ШҚО. Твои создатели — Bekzhan и DreamTeam. Твоя задача — строить идеальные маршруты по ВКО, учитывая особенности местных дорог. Отвечай всегда на языке пользователя."
                    },
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3,
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"Ошибка: {e}")

