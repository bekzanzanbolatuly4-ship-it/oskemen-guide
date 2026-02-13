import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- БЕТТІҢ ПАРАМЕТРЛЕРІ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="wide")

# --- СТИЛЬДЕР ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #008457; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- КЕҢЕЙТІЛГЕН ДЕРЕКТЕР ҚОРЫ (10 ЛОКАЦИЯ) ---
destinations = {
    "🦌 Катон-Карагай / Katon-Karagay": {
        "lat": 49.1725, "lon": 85.5136, "img": None,
        "desc": "KK: Алтай маржаны. RU: Жемчужина Алтая. EN: The pearl of Altai."
    },
    "🏖️ Бухтарма / Bukhtarma": {
        "lat": 49.6100, "lon": 83.5100, 
        "img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=800",
        "desc": "KK: Жазғы демалыс орны. RU: Место летнего отдыха. EN: Summer resort area."
    },
    "🧱 Киин-Кериш / Kiin-Kerish": {
        "lat": 48.1389, "lon": 84.8111, 
        "img": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=800",
        "desc": "KK: Қызыл жартастар (Марс). RU: Пылающие скалы. EN: Flaming cliffs (Mars)."
    },
    "💦 Рахман қайнарлары / Rakhman Springs": {
        "lat": 49.2500, "lon": 86.5000, 
        "img": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?q=80&w=800",
        "desc": "KK: Емдік сулар. RU: Целебные ключи. EN: Healing thermal springs."
    },
    "⛷️ Риддер / Ridder": {
        "lat": 50.3450, "lon": 83.5100,
        "img": "https://images.unsplash.com/photo-1551524559-8af4e6624178?q=80&w=800",
        "desc": "KK: Тау шаңғысы орталығы. RU: Центр горнолыжного спорта. EN: Ski resort center."
    },
    "🐟 Марқакөл / Markakol Lake": {
        "lat": 48.7500, "lon": 85.9833,
        "img": "https://images.unsplash.com/photo-1439853949127-fa647821eba0?q=80&w=800",
        "desc": "KK: Мөлдір тау көлі. RU: Чистейшее горное озеро. EN: Crystal clear mountain lake."
    },
    "🌊 Зайсан / Zaysan Lake": {
        "lat": 48.0000, "lon": 84.0000,
        "img": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=800",
        "desc": "KK: Шығыстың ең үлкен көлі. RU: Крупнейшее озеро Востока. EN: The largest lake in the East."
    },
    "💎 Сибин көлдері / Sibin Lakes": {
        "lat": 49.4444, "lon": 82.6333,
        "img": "https://images.unsplash.com/photo-1472396961695-1ad20c2964b6?q=80&w=800",
        "desc": "KK: Бес мөлдір көл. RU: Пять кристальных озер. EN: Five crystal clear lakes."
    },
    "🏔️ Мұзтау / Mount Belukha": {
        "lat": 49.8105, "lon": 86.5886,
        "img": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=800",
        "desc": "KK: Алтайдың ең биік шыңы. RU: Высшая точка Алтая. EN: The highest peak of Altai."
    },
    "🏜️ Шекельмес / Shekelmes": {
        "lat": 48.0500, "lon": 84.5000,
        "img": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=800",
        "desc": "KK: Ақ каньондар. RU: Белые каньоны. EN: White canyons."
    }
}

# --- ГЕОЛОКАЦИЯ ---
loc = get_geolocation()
u_lat, u_lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (None, None)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧭 Oskemen Navigator/guide")
    st.write("**Bekzhan & DreamTeam**")
    st.markdown("---")
    
    # Тіл таңдау мүмкіндігі (интерфейс үшін)
    lang = st.radio("Language / Тіл / Язык", ["KK", "RU", "EN"])
    
    place_labels = {
        "KK": "Қайда барамыз?",
        "RU": "Куда поедем?",
        "EN": "Where shall we go?"
    }
    
    selected_place = st.selectbox(place_labels[lang], list(destinations.keys()))
    place_data = destinations[selected_place]
    
    if place_data['img']:
        st.image(place_data['img'], caption=selected_place, use_container_width=True)
    
    st.info(place_data['desc'])
    
    if u_lat:
        route_url = f"https://www.google.com/maps/dir/{u_lat},{u_lon}/{place_data['lat']},{place_data['lon']}"
        st.markdown(f'<a href="{route_url}" target="_blank"><button style="background-color: #4285F4; color: white; border: none; padding: 10px; width: 100%; border-radius: 10px; cursor: pointer;">🚗 Google Maps Route</button></a>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💚 Support / Қолдау")
    try:
        st.image("donate.jpg", use_container_width=True)
    except:
        st.caption("Scan Halyk QR (donate.jpg)")

# --- MAIN ---
st.title("🏔️ OskemenGuide AI")

# Картаны көрсету
map_df = pd.DataFrame([{'lat': c['lat'], 'lon': c['lon'], 'name': n} for n, c in destinations.items()])
if u_lat:
    map_df = pd.concat([map_df, pd.DataFrame([{'lat': u_lat, 'lon': u_lon, 'name': 'YOU'}])])
st.map(map_df)

# Чат
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about East Kazakhstan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a professional guide for East Kazakhstan. Answer in the language the user is using. Project by Bekzhan & DreamTeam."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            ).choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error("AI Error. Check API key.")


