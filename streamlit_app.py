# 😂 배꼽봇: 고급 통합 버전
# 기능: 🌗 다크모드 감지, 📱 모바일 대응, 🧠 복사로그+AI학습, 🎨 테마선택, 📁 저장, 📤 공유

import streamlit as st
import random
import os
import html
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------- 설정 ----------------------
st.set_page_config(page_title="😂 배꼽봇", page_icon="😜", layout="wide")
st.title("😂 배꼽봇 (BaekkopBot)")

# ---------------------- 테마 설정 ----------------------
theme = st.sidebar.selectbox("🎨 테마 선택", ["기본", "다크", "자연", "파스텔"])

theme_styles = {
    "기본": {"bg": "#f39c12", "hover": "#d35400"},
    "다크": {"bg": "#444", "hover": "#666"},
    "자연": {"bg": "#27ae60", "hover": "#1e8449"},
    "파스텔": {"bg": "#f5b7b1", "hover": "#ec7063"},
}
colors = theme_styles.get(theme, theme_styles["기본"])

# ---------------------- API 키 ----------------------
api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")
if not api_key:
    st.warning("API 키를 입력하세요!")
    st.stop()

# ---------------------- 언어 선택 ----------------------
language = st.sidebar.selectbox("🌍 언어 선택", ["한국어", "English", "日本語"])
if language == "English":
    system_prompt = "You are BaekkopBot, a world-class humor chatbot."
elif language == "日本語":
    system_prompt = "あなたは世界最高のユーモアチャットボット『ベコッボット』です。"
else:
    system_prompt = "당신은 유쾌한 유머 챗봇 배꼽봇입니다. 웃음을 주세요!"

# ---------------------- 상태 초기화 ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.generated_text = ""
    st.session_state.saved_jokes = []
    st.session_state.copy_log = []

client = OpenAI(api_key=api_key)

# ---------------------- 예시 질문 ----------------------
example_questions = [
    "아재개그 하나만! 😂",
    "요즘 핫한 밈은? 🔥",
    "세계에서 제일 웃긴 농담은? 🤣"
]

st.markdown("#### 💬 이런 걸 물어보세요!")
for i, q in enumerate(example_questions):
    if st.button(f"💭 {q}", key=f"ex{i}"):
        st.session_state.messages.append({"role": "user", "content": q})

# ---------------------- 입력 ----------------------
user_input = st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(html.escape(user_input))

    # 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("배꼽 터지는 중... 🤣"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=150
            )
            full_text = response.choices[0].message.content
            st.session_state.generated_text = full_text
            st.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})

# ---------------------- 유머 표시 및 복사 ----------------------
if st.session_state.generated_text:
    st.markdown("---")
    st.text_area("📝 유머 내용", value=st.session_state.generated_text, height=150, disabled=True)

    # 자동 복사 JS 버튼
    st.markdown(f"""
    <div>
        <textarea id="copyText" style="position: absolute; left: -9999px;">{st.session_state.generated_text}</textarea>
        <button id="copyBtn" onclick="
            const text = document.getElementById('copyText').value;
            navigator.clipboard.writeText(text).then(() => {{
                const msg = document.createElement('div');
                msg.textContent = '📋 클립보드에 복사되었어요!';
                msg.style.position = 'fixed';
                msg.style.bottom = '30px';
                msg.style.right = '30px';
                msg.style.background = '{colors['bg']}';
                msg.style.color = 'white';
                msg.style.padding = '12px 18px';
                msg.style.borderRadius = '12px';
                msg.style.zIndex = 9999;
                document.body.appendChild(msg);
                setTimeout(() => msg.remove(), 2000);
            }});
        " style="
            padding: 10px 20px;
            background-color: {colors['bg']};
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
        " onmouseover="this.style.backgroundColor='{colors['hover']}';" onmouseout="this.style.backgroundColor='{colors['bg']}';">
            📋 감성 복사하기
        </button>
    </div>
    <script>
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            document.getElementById('copyBtn').style.backgroundColor = '{theme_styles['다크']['bg']}';
        }}
    </script>
    """, unsafe_allow_html=True)

    # 복사 로그 저장
    if st.session_state.generated_text not in st.session_state.copy_log:
        st.session_state.copy_log.append(st.session_state.generated_text)

    # 저장 버튼
    if st.button("📁 이 유머 저장하기"):
        st.session_state.saved_jokes.append(st.session_state.generated_text)
        with open("saved_jokes.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.saved_jokes, f, ensure_ascii=False, indent=2)
        st.success("저장 완료! saved_jokes.json에 저장됨")

    # 공유 버튼
    share_url = f"https://story.kakao.com/share?url=https://your-app.com&text={st.session_state.generated_text}"
    st.markdown(f"""
        <a href="{share_url}" target="_blank">
            <button style="background:#FEE500;padding:10px 20px;border:none;border-radius:12px;font-weight:bold;cursor:pointer;">
                📤 카카오톡으로 공유하기
            </button>
        </a>
    """, unsafe_allow_html=True)

# ---------------------- AI 학습용 로그 보기 ----------------------
with st.expander("📊 내가 복사한 유머 기록 보기"):
    st.write(st.session_state.copy_log)
