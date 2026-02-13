import streamlit as st
import google.generativeai as genai

# Подключаем ключ из Secrets (обязательно добавь его в настройках Streamlit Cloud!)
KEY = st.secrets["GEMINI_KEY"]

# Конфигурация страницы
st.set_page_config(page_title="OskemenGuide", page_icon="📍", layout="centered")

# Кастомный CSS, чтобы убрать лишние отступы и сделать чат симпатичнее
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stApp { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

def initialize_agent():
    """Настройка ИИ и системных инструкций"""
    genai.configure(api_key=KEY)
    
    # Личность нашего гида
    system_behavior = (
        "Ты — локальный эксперт по Восточному Казахстану. Твой тон: дружелюбный, "
        "но профессиональный. Ты знаешь всё о скрытых тропах Риддера, лучших базах "
        "Бухтармы и легендах Белухи. Отвечай кратко, но по делу. "
        "Важно: в конце сообщения всегда напоминай: 'Береги природу — забери мусор с собой!'"
    )
    
    # Пытаемся запустить модель
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_behavior
    )
    return model

# Заголовок
st.title("🏔️ OskemenGuide AI")
st.caption("Твой персональный проводник по красотам Восточного Казахстана")

try:
    bot = initialize_agent()

    # Хранилище истории сообщений
    if "history" not in st.session_state:
        st.session_state.history = []

    # Отображаем старые сообщения
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Поле для ввода
    if user_input := st.chat_input("Например: Как доехать до Рахмановских ключей?"):
        
        # Показываем вопрос пользователя
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Генерация ответа с индикатором загрузки
        with st.chat_message("assistant"):
            with st.spinner("Ищу информацию по ВКО..."):
                try:
                    chat_session = bot.start_chat(history=[])
                    response = chat_session.send_message(user_input)
                    
                    st.markdown(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                except Exception as error:
                    st.error("Упс! Связь с горами прервалась. Попробуй еще раз через минуту.")

except Exception as startup_error:
    st.warning("Настройку ключа API нужно завершить в панели управления Streamlit.")