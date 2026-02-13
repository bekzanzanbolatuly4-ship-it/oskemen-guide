import streamlit as st
import google.generativeai as genai

if "GEMINI_KEY" not in st.secrets:
    st.error("Missing GEMINI_KEY in Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

@st.cache_resource
def load_model():
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
            full_prompt = f"Ты гид по Восточному Казахстану. Ответь на вопрос: {prompt}. В конце напомни про мусор."
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
