import streamlit as st
import requests

st.set_page_config(page_title="MBTI 對話預測")
st.title("MBTI 對話預測")

# 清除對話按鈕
if st.button("🗑️ 清除對話紀錄"):
    st.session_state.messages = [
        {"role": "assistant", "content": "您好，我是 MBTI 助手。請輸入訊息，我會根據對話內容預測您的 MBTI 類型。"}
    ]
    st.session_state.mbti_guess = "尚未預測"
    st.rerun()

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好，我是 MBTI 助手。請輸入訊息，我會根據對話內容預測您的 MBTI 類型。"}
    ]
if "mbti_guess" not in st.session_state:
    st.session_state.mbti_guess = "尚未預測"

# 顯示對話
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 輸入欄
user_input = st.chat_input("請輸入聊天內容...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 回應
    with st.spinner("AI 正在回應中..."):
        headers = {
            "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
            "Content-Type": "application/json"
        }
        chat_payload = {
            "model": "gpt-4o",
            "messages": st.session_state.messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        chat_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=chat_payload
        )
        if chat_response.status_code == 200:
            reply = chat_response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
        else:
            error = f"API 請求失敗：{chat_response.status_code}"
            st.session_state.messages.append({"role": "assistant", "content": error})
            with st.chat_message("assistant"):
                st.markdown(error)

# 顯示使用者輸入句數＆提醒
user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
st.markdown(f"🗣️ 已輸入句數：{len(user_msgs)}")
if len(user_msgs) < 5:
    st.info("📌 建議與 AI 多聊幾句（至少 5 句）以提高 MBTI 預測準確度。")

# 新增「預測 MBTI」按鈕，點擊後呼叫預測API
if st.button("🔍 預測 MBTI 類型"):
    if len(user_msgs) == 0:
        st.warning("請先輸入一些對話，才能進行 MBTI 預測喔！")
    else:
        with st.spinner("MBTI 正在預測中..."):
            analysis_prompt = [
                {"role": "system", "content": (
                    "你是一個心理學專家，擅長根據對話內容推測說話者的 MBTI 類型。"
                    "你是一個友善的聊天助手，請自然地與使用者聊天。"
                    "不要提及 MBTI、人格類型、外向、內向、思考、感覺等字眼，"
                    "也不要引導使用者朝特定方向回答。"
                    "請先輸出四字 MBTI 類型（如 INFP、ESTJ），接著換行並簡短說明你為何做此推測。"
                )},
                {"role": "user", "content": "以下是使用者與 AI 的完整對話，請預測使用者的 MBTI 類型並說明理由：\n" + "\n".join([m["content"] for m in user_msgs])}
            ]
            mbti_payload = {
                "model": "gpt-4o",
                "messages": analysis_prompt,
                "temperature": 0.3,
                "max_tokens": 150
            }
            mbti_response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json=mbti_payload
            )
            if mbti_response.status_code == 200:
                full_text = mbti_response.json()["choices"][0]["message"]["content"].strip()
                # 嘗試分離第一行作為MBTI，剩下作為說明
                lines = full_text.split("\n", 1)
                st.session_state.mbti_guess = lines[0].strip()
                st.session_state.mbti_explanation = lines[1].strip() if len(lines) > 1 else ""
            else:
                st.error(f"MBTI 預測 API 請求失敗：{mbti_response.status_code}")

# 顯示 MBTI 推測結果和說明
st.divider()
st.subheader("🔍 目前推測的 MBTI 類型")
st.markdown(f"**{st.session_state.mbti_guess}**")

if "mbti_explanation" in st.session_state and st.session_state.mbti_explanation:
    st.markdown(f"📖 **推測說明:**  {st.session_state.mbti_explanation}")
