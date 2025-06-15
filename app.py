import streamlit as st
import requests

st.set_page_config(page_title="MBTI 對話預測")
st.title("MBTI 對話預測")

# 儲存對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好，我是 AI 助手。請開始輸入任何訊息，我會協助預測您的 MBTI。"}
    ]

# 顯示過往對話
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 使用者輸入
user_input = st.chat_input("輸入訊息...")

if user_input:
    # 顯示使用者輸入
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 呼叫 OpenAI API
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
    else:
        error_msg = f"❌ API 請求失敗：{response.status_code}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.markdown(error_msg)
