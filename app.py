import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")
st.subheader("Безопасное подключение через Secrets")

# 2. Получение ключа из Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("Ошибка: Ключ GROQ_API_KEY не найден в Secrets!")
    st.stop()

# Инициализация клиента через секреты
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. История чата
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. Логика чата
if prompt := st.chat_input("Спроси про ВКО..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "Ты гид по Восточному Казахстану. Отвечай кратко на русском."},
                    {"role": "user", "content": prompt}
                ],
            )
            
            response_text = completion.choices[0].message.content
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
