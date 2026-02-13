import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- БЕТТІҢ ПАРАМЕТРЛЕРІ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛЬДЕР (CSS) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #008457; color: white; }
    .main-title { font-size: 3rem; font-weight: bold; color: #1E1E1E; }
    </style>
""", unsafe_allow_html=True)

# --- ДЕРЕКТЕР ҚОРЫ (Локациялар, Фотолар және Сипаттама) ---
destinations = {
    "🦌 Катон-Карагай": {
        "lat": 49.1725, "lon": 85.5136, 
        "img": "https://images.unsplash.com/photo-1589405709100-36a591321703?q=80&w=800",
        "desc": "Қазақстанның Алтайы, маралдар мен бал қарағайлар мекені."
    },
    "🏖️ Бухтарма": {
        "lat": 49.6100, "lon": 83.5100, 
        "img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=800",
        "desc": "Таулар арасындағы алып теңіз."
    },
    "🧱 Киин-Кериш": {
        "lat": 48.1389, "lon": 84.8111, 
        "img": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=800",
        "desc": "Марс пейзажын еске түсіретін отты жартастар."
    },
    "💦 Рахмановские ключи": {
        "lat": 49.2500, "lon": 86.5000, 
        "img": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?q=80&w=800",
        "desc": "1760 метр биіктіктегі емдік бұлақтар."
    },
    "⛷️ Риддер (Ивановский белок)": {
        "lat": 50.3450, "lon": 83.5100,
        "img": "https://images.unsplash.com/photo-1551524559-8af4e6624178?q=80&w=800",
        "desc": "Қысқы спорт пен таза ауа орталығы."
    }
}

# --- ГЕОЛОКАЦИЯ АНЫҚТАУ ---
loc = get_geolocation()
u_lat, u_lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (None, None)

# --- SIDEBAR (БАСҚАРУ ПАНЕЛІ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=100)
    st.title("🧭 Oskemen Navigator")
    st.write("Команда: **Bekzhan & DreamTeam**")
    st.markdown("---")
    
    # Орын таңдау
    selected_place = st.selectbox("Қайда барамыз?", list(destinations.keys()))
    place_data = destinations[selected_place]
    
    # Фото және Сипаттама
    st.image(place_data['img'], caption=selected_place, use_container_width=True)
    st.info(place_data['desc'])
    
    # Google Maps Маршрут батырмасы
    if u_lat:
        route_url = f"https://www.google.com/maps/dir/{u_lat},{u_lon}/{place_data['lat']},{place_data['lon']}"
        st.markdown(f'<a href="{route_url}" target="_blank"><button style="background-color: #4285F4; color: white; border: none; padding: 10px; width: 100%; border-radius: 10px; cursor: pointer;">🗺️ Google Maps-те ашу</button></a>', unsafe_allow_html=True)
    else:
        st.warning("📍 Маршрут құру үшін геопозицияға рұқсат беріңіз.")

    # HALYK QR БЛОГЫ
    st.markdown("---")
    st.subheader("💚 Жобаны қолдау")
    st.image("https://photos.app.goo.gl/uStXL2xGpEKA8iEf6", caption="Halyk QR сканерлеңіз", use_container_width=True)
    st.markdown('<div style="background-color: #008457; color: white; padding: 10px; border-radius: 10px; text-align: center;">Halyk Bank 💳</div>', unsafe_allow_html=True)

# --- НЕГІЗГІ БЕТ ---
st.title("🏔️ OskemenGuide AI")
st.write(f"Сәлем! Мен сіздің ШҚО бойынша ақылды көмекшіңізбін.")

# Интерактивті карта
map_list = []
for name, coords in destinations.items():
    map_list.append({'lat': coords['lat'], 'lon': coords['lon'], 'name': name})
if u_lat:
    map_list.append({'lat': u_lat, 'lon': u_lon, 'name': 'СІЗ ОСЫНДАСЫЗ'})

st.map(pd.DataFrame(map_list))

# Чат интерфейсі
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Сұрақ енгізу
if prompt := st.chat_input("ШҚО туралы не білгіңіз келеді?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Сен Шығыс Қазақстан бойынша кәсіби гидсің. Жауаптарың нақты, сауатты және достық райда болсын. Бекжан және DreamTeam командасы жасаған жоба екенін ұмытпа."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Қате орын алды: {e}")
