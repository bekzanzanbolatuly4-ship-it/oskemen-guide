import streamlit as st
import requests

st.set_page_config(page_title="OskemenGuide AI", page_icon="🏔️")
st.title("🏔️ OskemenGuide AI")

# Твой API ключ
API_KEY = "AIzaSyBuXI1rAoCyDujcOSF7poXKZW1o_qozRhI"
# Прямая ссылка для запроса к Google
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Ввод сообщения
if prompt := st.chat_input("Спроси меня о Восточном Казахстане..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Формируем запрос
        payload = {
            "contents": [{
                "parts": [{"text": f"Ты профессиональный гид по ВКО. Отвечай кратко и интересно на вопрос: {prompt}"}]
            }]
        }
        
        try:
            # Отправляем запрос напрямую
            response = requests.post(URL, json=payload)
            data = response.json()
            
            # Проверяем ответ
            if "candidates" in data:
                answer = data["candidates"][0]["content"]["parts"][0]["text"]
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                # Если Google выдал ошибку (например, по региону), мы её увидим здесь
                error_msg = data.get("error", {}).get("message", "Неизвестная ошибка")
                st.error(f"Google ответил: {error_msg}")
        except Exception as e:
            st.error(f"Ошибка связи: {e}")

