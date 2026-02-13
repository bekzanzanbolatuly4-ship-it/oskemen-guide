import streamlit as st
from groq import Groq

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️", layout="centered")

st.title("🏔️ OskemenGuide AI")
st.caption("✨ by Bekzhan ✨")

st.markdown("""<style>.stChatMessage { border-radius: 15px; }</style>""", unsafe_allow_html=True)

if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Сұрағыңызды жазыңыз / Пишите ваш вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                # МЫ ПОСТАВИЛИ МОДЕЛЬ 70B - ОНА ЛУЧШЕ ЗНАЕТ КАЗАХСКИЙ
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Сен — Шығыс Қазақстан облысы бойынша кәсіби гидсің. "
                            "ПРАВИЛО 1: Если пользователь пишет на казахском, отвечай на чистом, литературном казахском языке (қазақ тілінде жауап бер). "
                            "ПРАВИЛО 2: Используй правильную грамматику и специфические термины ВКО. "
                            "ПРАВИЛО 3: Всегда отвечай на языке вопроса."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3, # Чуть-чуть добавим гибкости для красоты языка
            )
            
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Қате шықты / Ошибка: {e}")

with st.sidebar:
    st.header("OskemenGuide AI")
    st.write("🇰🇿 Қазақ тілі жақсартылды")
    st.write("👨‍💻 Автор: **Bekzhan**")
    if st.button("Тазалау / Очистить"):
        st.session_state.messages = []
        st.rerun()

