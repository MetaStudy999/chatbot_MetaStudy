import streamlit as st
import random
import json
import matplotlib.pyplot as plt
from openai import OpenAI

# ✅ 기본 설정
st.set_page_config(page_title="😂 배꼽봇", page_icon="😜")
st.title("😂 배꼽봇 (BaekkopBot)")
st.image("logo.png", caption="🌱 웃음 충전 중... 배꼽봇과 함께 😄", use_container_width=True)

# ✅ 말풍선 CSS
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

# ✅ 언어 선택
language = st.sidebar.selectbox("🌐 언어 선택 / Language", ["한국어", "English", "日本語"])
if language == "English":
    system_prompt = "You are BaekkopBot, a world-class humor chatbot. You greet users with clever, culturally sensitive jokes..."
elif language == "日本語":
    system_prompt = "あなたは世界最高のユーモアチャットボット『ベコッボット』です..."
else:
    system_prompt = """
    당신은 세계 최고로 창의적이고 유머 감각이 넘치는 AI 개그 챗봇입니다. 당신의 이름은 '배꼽봇'입니다.
    사용자에게 웃음을 주는 농담, 퀴즈, 밈 등을 상황에 맞게 유쾌하게 전달해 주세요.
    """

# ✅ OpenAI API 키
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", value=st.session_state.api_key)
if not openai_api_key:
    st.info("API 키를 입력해 주세요.", icon="🗝️")
    st.stop()
st.session_state.api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)

# ✅ 상태 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.saved_jokes = []
    st.session_state.style_scores = {"dad_joke": 0, "nonsense": 0, "dark": 0}
    st.session_state.greeted = False
    st.session_state.response_saved = False
    st.session_state.pending_prompt = None

# ✅ 예시 질문 & 인사
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

# ✅ 환영 인사 & 말풍선
if not st.session_state.greeted:
    with st.chat_message("assistant"):
        st.markdown(random.choice(greetings))
    st.markdown("#### 💬 이런 질문 해볼까요?")
    for i, q in enumerate(example_questions):
        if st.button(f"💭 {q}", key=f"btn{i}"):
            st.session_state.pending_prompt = q
            st.session_state.greeted = True
            st.rerun()

# ✅ 사이드바: 저장, 분석, 다운로드
with st.sidebar:
    st.markdown("### ⭐ 저장한 유머")
    for idx, joke in enumerate(st.session_state.saved_jokes, 1):
        st.markdown(f"{idx}. {joke}")

    st.markdown("### 🎯 유머 취향 분석")
    def get_humor_type(scores):
        if max(scores.values()) == 0:
            return "아직 취향을 파악 중이에요! 😊"
        top = max(scores, key=scores.get)
        label = {"dad_joke": "아재개그", "nonsense": "넌센스", "dark": "블랙유머"}
        return f"당신은 **{label[top]} 스타일** 유머를 좋아하시는군요! 😎"
    st.markdown(get_humor_type(st.session_state.style_scores))

    if st.button("📥 저장 유머 TXT"):
        text = "\n\n".join(st.session_state.saved_jokes)
        st.download_button("TXT 다운로드", text, file_name="saved_jokes.txt")

    if st.button("📥 저장 유머 JSON"):
        data = json.dumps({"jokes": st.session_state.saved_jokes}, ensure_ascii=False)
        st.download_button("JSON 다운로드", data, file_name="saved_jokes.json")

    fig, ax = plt.subplots()
    ax.bar(st.session_state.style_scores.keys(), st.session_state.style_scores.values(), color=["#f1c40f", "#2ecc71", "#e74c3c"])
    ax.set_title("유머 취향 점수")
    st.pyplot(fig)

# ✅ 이전 대화 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✅ 채팅 입력창 (항상 출력되도록)
prompt_input = st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂")

# ✅ GPT 응답 처리
prompt = st.session_state.pop("pending_prompt", None) or prompt_input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_response = ""
    copy_button = copy_col.button("📋 복사", key="copy_button")
    response_box = st.empty()

    with st.chat_message("assistant"):
        copy_col, response_col = st.columns([0.1, 0.9])
        with response_col:
            with st.spinner("배꼽 터지는 중... 🤣"):
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
            if copy_button and full_response:
                st.session_state.clipboard = full_response
                st.toast("복사되었습니다!", icon="📋")

    # ✅ 스트리밍 완료 후 저장 버튼 노출 및 디버깅 출력
    if full_response and not st.session_state.response_saved:
        st.write("DEBUG: 저장 버튼 활성화됨")
        if st.button("⭐ 이 유머 저장하기"):
            st.write("DEBUG: 저장 시도됨")
            st.write("DEBUG: full_response =", full_response)
            if full_response not in st.session_state.saved_jokes:
                st.session_state.saved_jokes.append(full_response)
                st.success("✅ 유머가 저장되었어요!")
            st.write("DEBUG: saved_jokes =", st.session_state.saved_jokes)
            st.session_state.response_saved = True

    humor = st.radio("유머 스타일을 선택해 주세요:",
                     ["😂 아재개그 스타일!", "😶 넌센스 같아요", "😈 블랙유머 느낌"],
                     index=None, key="humor_choice")
    if humor:
        if "아재개그" in humor:
            st.session_state.style_scores["dad_joke"] += 1
        elif "넌센스" in humor:
            st.session_state.style_scores["nonsense"] += 1
        elif "블랙유머" in humor:
            st.session_state.style_scores["dark"] += 1

    st.session_state.messages.append({"role": "assistant", "content": full_response})
