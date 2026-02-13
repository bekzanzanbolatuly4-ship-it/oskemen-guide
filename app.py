import streamlit as st
import pandas as pd
from groq import Groq
from streamlit_js_eval import get_geolocation

# --- SEO ЖӘНЕ КОНФИГУРАЦИЯ ---
st.set_page_config(
    page_title="Oskemen Navigator v2.0",
    page_icon="🧭",
    layout="wide"
)

# Google Verification
st.markdown('<meta name="google-site-verification" content="google7a49481bcf67fe79" />', unsafe_allow_html=True)

# --- ДЕРЕКТЕР ҚОРЫ ---
# 1. Туристік орындар
locations = {
    "🦌 Катон-Карагай": {"lat": 49.1725, "lon": 85.5136, "type": "Табиғат", "desc": "Ұлттық парк, Мұзтау, Рахман қайнарлары."},
    "🏖️ Бухтарма": {"lat": 49.6100, "lon": 83.5100, "type": "Демалыс", "desc": "Шомылу, балық аулау және демалыс базалары."},
    "🧱 Киин-Кериш": {"lat": 48.1389, "lon": 84.8111, "type": "Экспедиция", "desc": "Марс пейзажды қызыл каньондар."},
    "⛷️ Риддер (Ивановский)": {"lat": 50.3450, "lon": 83.5100, "type": "Спорт", "desc": "Тау шаңғысы, фрирайд және Ивановский белок."},
    "🐟 Марқакөл": {"lat": 48.7500, "lon": 85.9833, "type": "Табиғат", "desc": "Қорық аймағы, мөлдір таза тау көлі."},
    "🏜️ Шекельмес": {"lat": 48.0500, "lon": 84.5000, "type": "Экспедиция", "desc": "Зайсан жағасындағы ақ каньондар."},
    "🌊 Сибин көлдері": {"lat": 49.4444, "lon": 82.6333, "type": "Демалыс", "desc": "Гранитті таулар арасындағы 5 мөлдір көл."},
    "🏔️ Мұзтау (Белуха)": {"lat": 49.8105, "lon": 86.5886, "type": "Альпинизм", "desc": "Алтайдың ең биік нүктесі."},
    "🦅 Алакөл (ШҚО жағы)": {"lat": 45.9667, "lon": 81.5833, "type": "Емдік", "desc": "Тұзды, емдік суы бар танымал көл."},
    "🗿 Ақбауыр": {"lat": 49.7214, "lon": 82.6847, "type": "Тарих", "desc": "Ежелгі обсерватория және петроглифтер."}
}

# 2. Отельдер мен Демалыс базалары
hotels = {
    "Өскемен": [
        {"name": "Shiny River", "stars": "⭐⭐⭐⭐", "link": "https://2gis.kz/ustkamenogorsk/search/hotels"},
        {"name": "Best Western Plus", "stars": "⭐⭐⭐⭐", "link": "https://2gis.kz/ustkamenogorsk/search/hotels"},
        {"name": "Dedeman Oskemen", "stars": "⭐⭐⭐⭐", "link": "https://2gis.kz/ustkamenogorsk/search/hotels"}
    ],
    "Катон-Карагай": [
        {"name": "Altai Resort", "stars": "Premium", "link": "https://2gis.kz/"},
        {"name": "Ясная Поляна", "stars": "Guest House", "link": "https://2gis.kz/"}
    ],
    "Бухтарма": [
        {"name": "Голубой Залив", "stars": "⭐⭐⭐", "link": "https://2gis.kz/"},
        {"name": "Айна", "stars": "Family", "link": "https://2gis.kz/"}
    ],
    "Риддер": [
        {"name": "Altai Alps", "stars": "Ski Resort", "link": "https://2gis.kz/"},
        {"name": "Altay Forest", "stars": "Eco Hotel", "link": "https://2gis.kz/"}
    ]
}

# --- ГЕОЛОКАЦИЯ ---
loc = get_geolocation()
u_lat, u_lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (None, None)

# --- SIDEBAR НАВИГАЦИЯ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=80)
    st.title("🏔️ VKO Super Navigator")
    st.info("Version 2.0.0 | DreamTeam Update")
    
    menu = st.selectbox("Бөлімді таңдаңыз:", 
                        ["🏠 Басты бет", "🗺️ Навигатор", "🏨 Отельдер", "🚐 Турлар", "🤖 AI Консультант"])
    
    st.markdown("---")
    st.subheader("💚 Қолдау көрсету")
    try:
        st.image("donate.jpg", caption="Halyk QR", use_container_width=True)
    except:
        st.write("QR суретін (donate.jpg) жүктеңіз")

# --- 🏠 БАСТЫ БЕТ ---
if menu == "🏠 Басты бет":
    st.title("🏔️ Шығыс Қазақстанға қош келдіңіз!")
    st.write("Бұл қосымша — сіздің ШҚО бойынша ең үздік көмекшіңіз. Барлық қызықты жерлер, отельдер мен маршруттар бір жерде.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Локациялар", "10+")
    col2.metric("Отельдер", "20+")
    col3.metric("Турлар", "5+")
    
    st.image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1200", caption="Ұлы Алтай таулары")

# --- 🗺️ НАВИГАТОР ---
elif menu == "🗺️ Навигатор":
    st.header("🗺️ Карта және Маршруттар")
    
    place_name = st.selectbox("Нүктені таңдаңыз:", list(locations.keys()))
    data = locations[place_name]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(place_name)
        st.write(f"**Түрі:** {data['type']}")
        st.write(f"**Сипаттама:** {data['desc']}")
        
        if u_lat:
            gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={u_lat},{u_lon}&destination={data['lat']},{data['lon']}"
            st.markdown(f'<a href="{gmaps_url}" target="_blank"><button style="width:100%; height:40px; background-color:#4285F4; color:white; border:none; border-radius:10px;">🚗 Google Maps Маршрут</button></a>', unsafe_allow_html=True)

    with col2:
        df = pd.DataFrame([{"lat": data["lat"], "lon": data["lon"], "name": place_name}])
        st.map(df)

# --- 🏨 ОТЕЛЬДЕР ---
elif menu == "🏨 Отельдер":
    st.header("🏨 ШҚО үздік отельдері мен демалыс базалары")
    city = st.selectbox("Аймақты таңдаңыз:", list(hotels.keys()))
    
    for hotel in hotels[city]:
        with st.expander(f"{hotel['name']} ({hotel['stars']})"):
            st.write(f"Жайлылық деңгейі: {hotel['stars']}")
            st.markdown(f"[2GIS-те көру және брондау]({hotel['link']})")

# --- 🚐 ТУРЛАР ---
elif menu == "🚐 Турлар":
    st.header("🚐 Дайын туристік пакеттер")
    st.warning("Кеңес: Турды кемінде 2 апта бұрын брондаған жөн.")
    
    tours = [
        {"name": "Алтай алтыны (Катон-Карагай)", "price": "95,000 ₸", "duration": "3 күн"},
        {"name": "Марсқа саяхат (Киин-Кериш)", "price": "70,000 ₸", "duration": "2 күн"},
        {"name": "Риддер фрирайды", "price": "55,000 ₸", "duration": "1 күн"}
    ]
    
    for tour in tours:
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"**{tour['name']}**")
        col2.write(tour['price'])
        col3.write(tour['duration'])
        st.divider()

# --- 🤖 AI КОНСУЛЬТАНТ ---
elif menu == "🤖 AI Консультант":
    st.header("🤖 Смарт Гид (LLama 3.3)")
    st.write("Кез келген сұрақ қойыңыз: 'Қай отель арзан?', 'Катонға қалай барамын?', 'Ең әдемі жер қайда?'")
    
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
                        {"role": "system", "content": "Сен Шығыс Қазақстанның SuperApp гидісің. Отельдер, жерлер, бағалар туралы бәрін білесің. Бекжан мен DreamTeam жасаған жоба."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                ).choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API Error")
