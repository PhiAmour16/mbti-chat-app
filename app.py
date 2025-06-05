import streamlit as st
import requests
import json

st.title("MBTI 對話預測（Hugging Face）")

user_input = st.text_input("請輸入一段自然對話：")

if user_input:
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
    payload = {
        "inputs": f"以下是對話內容：{user_input}，請猜測說話者可能的 MBTI 類型並簡要解釋。",
        "parameters": {"max_new_tokens": 100}
    }

    with st.spinner("模型思考中..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            try:
                result = response.json()
                output = result[0]["generated_text"]
                st.subheader("模型回應：")
                st.write(output)
            except Exception as e:
                st.error("⚠️ JSON 解碼錯誤，可能模型尚未啟動或回傳格式錯誤。")
                st.text("回傳原始內容：")
                st.code(response.text)
        else:
            st.error(f"❌ 錯誤狀態碼：{response.status_code}")
            st.text("回傳原始內容：")
            st.code(response.text)
