import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы (должна быть в самом верху)
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

# 2. Настройка ключа (Пробуем сначала Secrets, если нет — используем прямой)
if "GEMINI_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_KEY"]
else:
    # Твой новый ключ, который ты скинул
    API_KEY = "AIzaSyBuXI1rAoCyDujcOSF7poXKZW1o_qozRhI"

genai.configure(api_key=API_KEY)

# 3. Функция загрузки модели
@st.cache_resource
def load_model():
    # Пробуем разные имена модели, чтобы избежать 404
    for name in ["models/gemini-1.5-flash", "gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(name)
            # Тестовая проверка связи
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

# 4. Проверка подключения
if not model:
    st.error("Ошибка: Модель недоступна. Проверь API ключ и интернет-соединение.")
    st.stop()

# 5. Логика чата
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
            # Промпт для гида
            response = model.generate_content(f"Ты гид по Восточному Казахстану. Ответь кратко: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
