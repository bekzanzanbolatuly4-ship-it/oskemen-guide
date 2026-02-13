import streamlit as st
import google.generativeai as genai


api_key = "AIzaSyBuXI1rAoCyDujcOSF7poXKZW1o_qozRhI" 
genai.configure(api_key=api_key)

st.title("🏔️ OskemenGuide AI")

def load_model():
    try:
        # Пробуем только самый стабильный вариант
        m = genai.GenerativeModel('gemini-1.5-flash')
        return m
    except Exception as e:
        st.error(f"Техническая ошибка: {e}")
        return None

model = load_model()

import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

if "GEMINI_KEY" not in st.secrets:
    st.error("Добавь GEMINI_KEY в Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

@st.cache_resource
def load_model():
    # Пробуем 3 разных способа обращения к модели
    # Один из них точно сработает в зависимости от версии API
    for name in ["models/gemini-1.5-flash", "gemini-1.5-flash", "gemini-pro"]:
        try:
            m = genai.GenerativeModel(name)
            m.generate_content("test") # Проверка связи
            return m
        except:
            continue
    return None

model = load_model()

if not model:
    st.error("Не удалось подключить модель. Проверь API ключ в Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Спроси про ВКО..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Твой промпт для гида
            res = model.generate_content(f"Ты гид по ВКО. Ответь кратко: {prompt}")
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
