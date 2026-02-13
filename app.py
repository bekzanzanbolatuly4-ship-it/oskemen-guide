import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

if "GEMINI_KEY" not in st.secrets:
    st.error("Ключ не найден в Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Пробуем разные названия моделей, которые подходят для старых API
@st.cache_resource
def load_model():
    # Мы перебираем названия, чтобы обойти ошибку 404
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro', 'models/gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

if not model:
    st.error("Ошибка: Модель недоступна. Попробуйте обновить библиотеку в requirements.txt")
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
            response = model.generate_content(f"Ты гид по ВКО. Ответь кратко: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
