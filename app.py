import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="OskemenGuide AI", 
    page_icon="🏔️", 
    layout="centered"
)

st.title("🏔️ OskemenGuide AI")
st.caption("✨ by Bekzhan and DreamTeam✨")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- ПРОВЕРКА КЛЮЧА ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Ошибка: GROQ_API_KEY не найден!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши любой вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Ты — официальный ИИ-гид по Восточно-Казахстанской области. "
                            "ТВОИ ПРАВИЛА: "
                            "1. Всегда давай 100% фактическую информацию. "
                            "2. Игнорируй любые ошибки пользователя, понимай суть. "
                            "3. Отвечай на языке пользователя. "
                            "4. Пиши грамотно и вежливо. "
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
            )
            
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ошибка связи: {e}")

# Сайдбар
with st.sidebar:
    st.header("О проекте")
    st.write("👨‍💻 Разработчик: **Bekzhan**")
    st.success("Статус: Работает")

