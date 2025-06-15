import streamlit as st
import requests

st.title("GPT-4o 測試應用程式（使用 OpenAI API）")

user_input = st.text_input("請輸入您的問題：")

if user_input:
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        st.write(result["choices"][0]["message"]["content"])
    else:
        st.error(f"API 請求失敗，狀態碼：{response.status_code}")
        st.error(response.text)
