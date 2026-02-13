import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- НАСТРОЙКА ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛИ ---
st.markdown("""<style>.stChatMessage { border-radius: 15px; } .stButton>button { width: 100%; border-radius: 8px; }</style>""", unsafe_allow_html=True)

# --- ГЕОЛОКАЦИЯ ---
st.sidebar.title("📍 Ваша локация")
loc = get_geolocation() # Запрос геопозиции у браузера

user_lat, user_lon = None, None
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']
    st.sidebar.success(f"Координаты получены: {user_lat:.4f}, {user_lon:.4f}")
else:
    st.sidebar.warning("Пожалуйста, разрешите доступ к геопозиции для построения маршрутов.")

# --- ДАННЫЕ МЕСТ ---
destinations = {
    "Сибинские озёра": {"lat": 49.4329, "lon": 82.6571, "dist_info": "~72 км от Усть-Каменогорска"},
    "Бухтарма": {"lat": 49.5735, "lon": 83.5612, "dist_info": "~100 км от Усть-Каменогорска"},
    "Катон-Карагай": {"lat": 49.1725, "lon": 85.5136, "dist_info": "~350 км от Усть-Каменогорска"}
}

# --- ПРОВЕРКА API КЛЮЧА ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.subheader("🚀 Developed by Bekzhan & DreamTeam")
    st.markdown("---")
    st.subheader("🗺️ Построить маршрут:")
    
    selected_route = None
    for place in destinations:
        if st.button(f"🚗 До {place}"):
            if user_lat and user_lon:
                selected_route = f"Я нахожусь здесь: {user_lat}, {user_lon}. Построй маршрут до {place}. Сколько ехать и какая дорога?"
            else:
                selected_route = f"Расскажи маршрут из Усть-Каменогорска до {place}. (Геопозиция не определена)"

# --- ОСНОВНОЙ БЛОК ---
st.title("🏔️ OskemenGuide AI")
st.caption("✨ by Bekzhan & DreamTeam")

# Карта
map_data = pd.DataFrame(list(destinations.values()))
if user_lat: # Добавляем пользователя на карту
    user_point = pd.DataFrame([{'lat': user_lat, 'lon': user_lon, 'name': 'Вы здесь'}])
    st.map(pd.concat([map_data, user_point]))
else:
    st.map(map_data)

# Чат
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Спроси дорогу...")
final_prompt = prompt or selected_route

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"): st.markdown(final_prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Ты гид-навигатор. Если есть координаты пользователя, рассчитай примерное время и опиши путь. Отвечай на языке запроса."},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3,
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"Ошибка: {e}")
