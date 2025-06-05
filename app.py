import streamlit as st
import requests

st.title("GPT-4o 測試應用程式")

user_input = st.text_input("請輸入您的問題：")

if user_input:
    headers = {
        "Authorization": f"Bearer {st.secrets['GITHUB_API_TOKEN']}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": user_input,
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 100
        }
    }

    response = requests.post(st.secrets["MODEL_API_URL"], headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.write(result.get("generated_text", "未取得回應"))
    else:
        st.error(f"API 請求失敗，狀態碼：{response.status_code}")
