import streamlit as st
import requests

st.title("MBTI 對話預測（ChatYuan v2）")

user_input = st.text_input("請輸入一段自然對話內容：")

if user_input:
    API_URL = "https://api-inference.huggingface.co/models/ClueAI/ChatYuan-large-v2"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
    }

    # 指令提示語，加強任務導向（MBTI 預測）
    prompt = f"根據這段中文對話，請猜測這個人的 MBTI 類型並簡要說明原因：{user_input}"

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100}
    }

    with st.spinner("思考中..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            try:
                result = response.json()
                st.subheader("模型回應：")
                st.write(result[0]["generated_text"])
            except Exception as e:
                st.error("⚠️ 模型回傳格式解析失敗。")
                st.code(response.text)
        else:
            st.error(f"❌ API 錯誤，狀態碼：{response.status_code}")
            st.code(response.text)
