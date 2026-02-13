import streamlit as st
from groq import Groq

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="OskemenGuide AI by Bekzhan", 
    page_icon="🏔️", 
    layout="centered"
)

# Стилизация заголовка
st.title("🏔️ OskemenGuide AI by Bekzhan")
st.markdown("### Твой персональный гид по Восточному Казахстану")
st.info("Спроси меня о достопримечательностях Усть-Каменогорска, Катон-Карагая или Бухтармы!")

# --- ПРОВЕРКА КЛЮЧА ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Ошибка: Ключ GROQ_API_KEY не найден в Secrets!")
    st.info("Добавьте ключ в настройках Streamlit Cloud: GROQ_API_KEY = 'ваш_ключ'")
    st.stop()

# Инициализация клиента Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- РАБОТА С ИСТОРИЕЙ ЧАТА ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображаем старые сообщения
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ПОЛЕ ВВОДА ---
if prompt := st.chat_input("Напишите ваш вопрос здесь..."):
    # Добавляем сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ответ ИИ
    with st.chat_message("assistant"):
        try:
            # Используем актуальную модель Llama 3.1
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Ты — экспертный гид по Восточно-Казахстанской области (ВКО) и городу Усть-Каменогорск. "
                            "Отвечай вежливо, кратко и только на русском языке. "
                            "Если тебя спрашивают о местах, старайся давать полезные советы для туристов."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            
            # Сохраняем ответ в историю
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Произошла ошибка при обращении к ИИ: {e}")

