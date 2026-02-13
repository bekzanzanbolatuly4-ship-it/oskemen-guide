import streamlit as st
import google.generativeai as genai

# Твой ключ
API_KEY = st.secrets["GEMINI_KEY"]

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

try:
    genai.configure(api_key=API_KEY)
    
    # 1. АВТОПОДБОР: Эта штука сама найдет, как называется модель у тебя
    if "model_name" not in st.session_state:
        # Просим у Google список всех моделей, которые работают с твоим ключом
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if models:
            # Выбираем самую свежую (flash или pro)
            st.session_state.model_name = models[0] 
        else:
            st.error("Ключ рабочий, но доступных моделей нет. Подожди 5 минут.")

    if "model_name" in st.session_state:
        # 2. Запускаем ту модель, которую нашли
        model = genai.GenerativeModel(st.session_state.model_name)
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
            st.session_state.messages = []
            # Приветствие
            st.session_state.messages.append({"role": "assistant", "content": "Салам! Я гид по ВКО. Куда рванем? 🏔️"})

        # Отображение чата
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Поле ввода
        if prompt := st.chat_input("Спроси про отдых в ВКО..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                # Генерируем ответ
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Бро, тут косяк с подключением: {e}")