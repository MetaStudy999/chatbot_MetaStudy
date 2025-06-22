import streamlit as st
import random
import os
import json
import html
from openai import OpenAI
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 기본 설정
st.set_page_config(page_title="😂 배꼽봇", page_icon="😜")
st.title("😂 배꼽봇 (BaekkopBot)")

# 로고 이미지 로드
try:
    st.image("logo.png", caption="🌱 웃음 충전 중... 배꼽봇과 함께 😄", use_container_width=True)
except FileNotFoundError:
    st.warning("로고 이미지를 찾을 수 없습니다!")

# 말풍선 CSS
st.markdown("""
<style>
.balloon-btn {
    display: block;
    padding: 0.6em 1em;
    margin: 0.3em 0;
    border: none;
    border-radius: 20px;
    background-color: #f39c12;
    color: white;
    font-weight: bold;
    cursor: pointer;
    text-align: left;
    transition: background 0.3s;
}
.balloon-btn:hover {
    background-color: #d35400;
}
</style>
""", unsafe_allow_html=True)

# 언어 선택
language = st.sidebar.selectbox("🌐 언어 선택 / Language", ["한국어", "English", "日本語"])
if language == "English":
    system_prompt = "You are BaekkopBot, a world-class humor chatbot. You greet users with clever, culturally sensitive jokes..."
elif language == "日本語":
    system_prompt = "あなたは世界最高のユーモアチャットボット『ベコッボット』です..."
elif language == "한국어":
    system_prompt = """
    당신은 세계 최고로 창의적이고 유머 감각이 넘치는 AI 개그 챗봇입니다. 당신의 이름은 '배꼽봇'입니다.
    사용자에게 웃음을 주는 농담, 퀴즈, 밈 등을 상황에 맞게 유쾌하게 전달해 주세요.
    """
else:
    st.error("지원되지 않는 언어입니다.")
    st.stop()

# OpenAI API 키 처리
api_key_env = os.getenv("OPENAI_API_KEY")
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", value=api_key_env or "")
if not openai_api_key:
    st.info("API 키를 입력해 주세요.", icon="🗝️")
    st.stop()
if "openai_client" not in st.session_state:
    try:
        st.session_state.openai_client = OpenAI(api_key=openai_api_key)
    except Exception as e:
        st.error(f"OpenAI API 키가 유효하지 않습니다: {str(e)}")
        st.stop()
client = st.session_state.openai_client

# 상태 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.max_messages = 30
    st.session_state.saved_jokes = []
    st.session_state.style_scores = {"dad_joke": 0, "nonsense": 0, "dark": 0}
    st.session_state.greeted = False
    st.session_state.response_saved = False
    st.session_state.pending_prompt = None
    # 저장된 농담 로드
    try:
        with open("saved_jokes.json", "r") as f:
            st.session_state.saved_jokes = json.load(f)
    except FileNotFoundError:
        st.session_state.saved_jokes = []

# 환영 인사 및 예시 질문
greetings = [
    "🌱 지구를 아끼는 당신, 오늘도 배꼽은 챙기셨나요?",
    "🌍 환영합니다! 지구를 위한 작은 미소, 여기서 시작돼요.",
    "🌿 자연은 숨 쉬고, 당신은 웃고, 배꼽봇은 개그해요!"
]
example_questions = [
    "재밌는 퀴즈 하나 줘! 🤔",
    "요즘 제일 핫한 밈 알려줘 🔥",
    "아재개그 하나만 부탁해요 😂",
    "기분 안 좋을 때 들으면 좋은 유머 있어?",
    "세계에서 제일 웃긴 농담 알려줘!"
]

if not st.session_state.greeted:
    with st.chat_message("assistant"):
        st.markdown(random.choice(greetings))
    st.markdown("#### 💬 이런 질문 해볼까요?")
    for i, q in enumerate(example_questions):
        if st.button(f"💭 {q}", key=f"btn{i}", help=f"예시 질문: {q}"):
            st.session_state.pending_prompt = q
            st.session_state.greeted = True
            st.rerun()

# 항상 표시되는 대화 입력창
prompt_input = st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂")

# 채팅 처리
if prompt_input or st.session_state.pending_prompt:
    prompt = st.session_state.pop("pending_prompt", None) or prompt_input
    st.session_state.messages.append({"role": "user", "content": prompt})
    if len(st.session_state.messages) > st.session_state.max_messages:
        st.session_state.messages = st.session_state.messages[-st.session_state.max_messages:]
    with st.chat_message("user"):
        st.markdown(html.escape(prompt))  # 사용자 입력 이스케이프

    full_response = ""
    st.session_state.response_saved = False  # 저장 플래그 리셋
    with st.chat_message("assistant"):
        response_box = st.empty()
        with st.spinner("배꼽 터지는 중... 🤣"):
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        response_box.markdown(full_response)
            except Exception as e:
                st.error(f"OpenAI API 호출 중 오류 발생: {str(e)}")
                st.stop()

        if full_response:
            copy_col, response_col = st.columns([0.1, 0.9])
            if copy_col.button("📋 복사", key="copy_button", help="응답을 클립보드에 복사"):
                escaped_response = html.escape(full_response)
                st.components.v1.html(f"""
                    <script>
                    navigator.clipboard.writeText(`{escaped_response}`)
                        .then(() => alert("📋 복사되었습니다!"))
                        .catch(() => alert("복사에 실패했습니다."));
                    </script>
                """, height=0)

    if full_response and not st.session_state.response_saved:
        if st.button("⭐ 이 유머 저장하기", key="save_joke_button", help="이 유머를 저장"):
            logging.debug("저장 시도됨")
            logging.debug(f"full_response = {full_response}")
            if full_response not in st.session_state.saved_jokes:
                st.session_state.saved_jokes.append(full_response)
                try:
                    with open("saved_jokes.json", "w") as f:
                        json.dump(st.session_state.saved_jokes, f)
                    st.success("✅ 유머가 저장되었어요!")
                except Exception as e:
                    st.error(f"유머 저장 중 오류 발생: {str(e)}")
            logging.debug(f"saved_jokes = {st.session_state.saved_jokes}")
            st.session_state.response_saved = True

    humor = st.radio("유머 스타일을 선택해 주세요:", ["😂 아재개그 스타일!", "😶 넌센스 같아요", "😈 블랙유머 느낌"], index=None, key="humor_choice")
    if humor:
        if "아재개그" in humor:
            st.session_state.style_scores["dad_joke"] += 1
        elif "넌센스" in humor:
            st.session_state.style_scores["nonsense"] += 1
        elif "블랙유머" in humor:
            st.session_state.style_scores["dark"] += 1

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 저장된 농담 표시
if st.session_state.saved_jokes:
    with st.expander("💾 저장된 유머 보기", expanded=False):
        for i, joke in enumerate(st.session_state.saved_jokes):
            st.markdown(f"**유머 {i+1}**: {html.escape(joke)}")
            if st.button("🗑️ 삭제", key=f"delete_joke_{i}", help="이 유머 삭제"):
                st.session_state.saved_jokes.pop(i)
                try:
                    with open("saved_jokes.json", "w") as f:
                        json.dump(st.session_state.saved_jokes, f)
                    st.success("유머가 삭제되었습니다!")
                except Exception as e:
                    st.error(f"유머 삭제 중 오류 발생: {str(e)}")
                st.rerun()

# 유머 스타일 통계
if any(st.session_state.style_scores.values()):
    st.subheader("📊 유머 스타일 통계")
    st.bar_chart(st.session_state.style_scores)

# 대화 초기화 버튼
if st.button("🔄 대화 초기화", help="대화 기록과 상태 초기화"):
    st.session_state.clear()
    st.success("대화가 초기화되었습니다!")
    st.rerun()
