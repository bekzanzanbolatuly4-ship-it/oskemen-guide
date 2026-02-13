import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

if "GEMINI_KEY" not in st.secrets:
    st.error("Добавь GEMINI_KEY в Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

try:
    model = get_model()
except Exception as e:
    st.error(f"Ошибка модели: {e}")
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
            response = model.generate_content(f"Ты гид по Восточному Казахстану. Ответь кратко: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ошибка API: {e}")
