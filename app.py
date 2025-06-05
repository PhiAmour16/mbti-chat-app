import streamlit as st
import requests

st.title("MBTI 對話預測（使用 Hugging Face）")

user_input = st.text_input("請輸入一段自然對話：")

if user_input:
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
    payload = {
        "inputs": f"以下對話描述一個人的行為與想法，請猜測這個人可能的 MBTI 類型並簡要說明原因：{user_input}",
        "parameters": {"max_new_tokens": 100}
    }

    with st.spinner("模型思考中..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            try:
                result = response.json()
                st.subheader("模型回應：")
                st.write(result[0]["generated_text"])
            except Exception:
                st.error("⚠️ 模型回傳格式無法解析")
                st.code(response.text)
        else:
            st.error(f"❌ 錯誤狀態碼：{response.status_code}")
            st.text("回傳原始內容：")
            st.code(response.text)
