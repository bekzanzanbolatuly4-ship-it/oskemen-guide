import streamlit as st
import google.generativeai as genai

if "GEMINI_KEY" not in st.secrets:
    st.error("Missing GEMINI_KEY in Secrets")
    st.stop()

# Настройка API
genai.configure(api_key=st.secrets["GEMINI_KEY"])

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

@st.cache_resource
def load_model():
    # Пробуем разные варианты имени модели, чтобы избежать ошибки 404
    for model_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # Проверочный запрос
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

if not model:
    st.error("Не удалось подключиться к модели. Проверьте API ключ.")
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
            full_prompt = f"Ты гид по Восточному Казахстану. Ответь кратко: {prompt}. В конце напомни про мусор."
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка: {e}")
