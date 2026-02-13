import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

# 2. Прямая настройка ключа (без st.secrets)
API_KEY = "AIzaSyBuXI1rAoCyDujcOSF7poXKZW1o_qozRhI"
genai.configure(api_key=API_KEY)

# 3. Инициализация модели
@st.cache_resource
def load_model():
    # Пробуем разные варианты имен, один точно сработает
    for model_name in ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(model_name)
            # Тестовый запрос для проверки
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

# 4. Проверка
if model is None:
    st.error("Ошибка подключения к Google AI. Возможно, ключ неактивен или регион заблокирован.")
    st.stop()

# 5. История чата
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. Ввод пользователя
if prompt := st.chat_input("Напиши что-нибудь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Ты гид по Восточному Казахстану. Ответь кратко: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
