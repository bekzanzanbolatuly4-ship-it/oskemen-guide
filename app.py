import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

# Проверяем ключ
if "GEMINI_KEY" not in st.secrets:
    st.error("Добавьте GEMINI_KEY в Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# Функция с исправленным путем к модели
@st.cache_resource
def load_model():
    try:
        # В некоторых версиях нужно писать 'models/gemini-1.5-flash'
        # В некоторых просто 'gemini-1.5-flash'
        # Пробуем оба варианта
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        model.generate_content("test")
        return model
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

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
            # Твой персональный промпт
            full_prompt = f"Ты гид по Восточному Казахстану. Ответь кратко на вопрос: {prompt}. В конце напомни беречь природу."
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
