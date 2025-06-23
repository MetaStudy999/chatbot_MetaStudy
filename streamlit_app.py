import streamlit as st
import random
import os
import html
from openai import OpenAI
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="😂 배꼽봇", page_icon="😜", layout="wide")
st.title("😂 배꼽봇 (BaekkopBot)")

# 커스텀 CSS
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
    width: 100%;
}
.balloon-btn:hover {
    background-color: #d35400;
}
.stButton>button {
    border-radius: 10px;
    padding: 8px 16px;
}
.stSpinner > div {
    border-color: #f39c12 !important;
}
</style>
""", unsafe_allow_html=True)

# 로고 이미지
try:
    st.image("logo.png", caption="🌱 웃음 충전 중... 배꼽봇과 함께 😄", use_container_width=True)
except FileNotFoundError:
    st.warning("로고 이미지를 찾을 수 없습니다!")

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

# OpenAI API 키 입력
api_key_env = os.getenv("OPENAI_API_KEY")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password", value=api_key_env or "")
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
    st.session_state.style_scores = {"dad_joke": 0, "nonsense": 0, "dark": 0}
    st.session_state.greeted = False
    st.session_state.pending_prompt = None

# 첫 인사
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

# 사용자 입력
prompt_input = st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂", max_chars=500)

if prompt_input or st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt", None) or prompt_input
    if len(prompt) > 500:
        st.error("입력은 500자를 초과할 수 없습니다!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    if len(st.session_state.messages) > st.session_state.max_messages:
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-st.session_state.max_messages+1:]

    with st.chat_message("user"):
        st.markdown(html.escape(prompt))

    full_response = ""
    with st.chat_message("assistant"):
        response_box = st.empty()
        with st.spinner("배꼽 터지는 중... 🤣"):
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=150,
                    stream=True
                )
                collected_chunks = []
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        collected_chunks.append(content)
                        full_response = "".join(collected_chunks)
                        response_box.markdown(html.escape(full_response))
                if not full_response.strip():
                    full_response = "죄송해요! 유머를 찾는 데 실패했어요. 다른 질문을 시도해 보세요! 😅"
                    response_box.markdown(html.escape(full_response))
            except Exception as e:
                logging.error(f"API 오류: {str(e)}")
                st.error(f"OpenAI API 호출 중 오류 발생: {str(e)}. 로그를 확인하세요.")
                st.stop()

        # 복사할 텍스트 저장
        st.session_state["generated_text"] = full_response

# 복사 및 스타일 선택 영역 (오류 방지 포함)
if "generated_text" in st.session_state and st.session_state.generated_text:
    st.markdown("##### 🤖 배꼽봇의 응답")
    st.text_area("📝 유머 내용", value=st.session_state.generated_text, height=150, disabled=True)

    if st.button("📋 복사하기"):
        st.toast("복사되었습니다! 클립보드에서 확인해 보세요. 😊")

    humor = st.radio("유머 스타일을 선택해 주세요:", ["😂 아재개그 스타일!", "😶 넌센스 같아요", "😈 블랙유머 느낌"], index=None, key=f"humor_choice_{len(st.session_state.messages)}")
    if humor:
        if "아재개그" in humor:
            st.session_state.style_scores["dad_joke"] += 1
        elif "넌센스" in humor:
            st.session_state.style_scores["nonsense"] += 1
        elif "블랙유머" in humor:
            st.session_state.style_scores["dark"] += 1
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.generated_text})

# 통계 출력
if any(st.session_state.style_scores.values()):
    st.subheader("📊 유머 스타일 통계")
    st.bar_chart(st.session_state.style_scores)

# 대화 초기화
if st.button("🔄 대화 초기화", help="대화 기록과 상태 초기화"):
    st.session_state.clear()
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.success("대화가 초기화되었습니다!")
    st.rerun()
