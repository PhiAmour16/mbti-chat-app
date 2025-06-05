import streamlit as st
import requests

st.title("MBTI 對話預測（使用 Hugging Face 模型）")

user_input = st.text_input("請輸入聊天內容：")

if user_input:
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
    payload = {
        "inputs": f"請根據以下對話判斷使用者可能的 MBTI 類型：{user_input}",
        "parameters": {"max_new_tokens": 100}
    }

    with st.spinner("思考中..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        try:
            output = result[0]["generated_text"]
            st.subheader("模型回應：")
            st.write(output)
        except Exception as e:
            st.error("發生錯誤，請確認模型是否載入完成或稍後再試。")
            st.write(result)
