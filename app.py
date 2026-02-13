import streamlit as st
from groq import Groq

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="OskemenGuide AI", 
    page_icon="🏔️", 
    layout="centered"
)

# --- ВИШЕНКА НА ТОРТЕ ---
st.title("🏔️ OskemenGuide AI")
st.caption("✨ by Bekzhan ✨")

# --- СТИЛИЗАЦИЯ (чтобы выглядело серьезно) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_content_allowed=True)

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

# --- ЛОГИКА ЧАТА ---
if prompt := st.chat_input("Напиши любой вопрос (даже с ошибками)..."):
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
                            "1. Всегда давай 100% фактическую и точную информацию. Если не уверен в факте — честно скажи об этом. "
                            "2. Игнорируй любые орфографические и грамматические ошибки пользователя. Понимай суть вопроса, даже если слова написаны неверно. "
                            "3. Отвечай на том языке, на котором написан вопрос (русский, казахский, английский и др.). "
                            "4. Пиши грамотно, структурировано и вежливо. "
                            "5. Используй актуальные названия мест в ВКО."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1, # Минимальная креативность для максимальной точности
                max_tokens=1500,
            )
            
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"Ошибка связи: {e}")

# Сайдбар с инфо
with st.sidebar:
    st.header("О проекте")
    st.write("Этот ИИ понимает любые вопросы о нашем крае, даже если вы спешили и допустили ошибки в тексте.")
    st.markdown("---")
    st.write("👨‍💻 Разработчик: **Bekzhan**")
    st.success("Статус: Работает идеально")
