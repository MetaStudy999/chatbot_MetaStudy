import streamlit as st
import openai
import random
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="😂 배꼽봇", page_icon="😜")
st.title("😂 배꼽봇 (BaekkopBot)")

# 로고 이미지
st.image("logo.png", caption="🌱 웃음 충전 중... 배꼽봇과 함께 😄", use_container_width=True)

# 말풍선 스타일용 CSS
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
else:
    system_prompt = """
    당신은 세계 최고로 창의적이고 유머 감각이 넘치는 AI 개그 챗봇입니다. 당신의 이름은 '배꼽봇'입니다.
    사용자에게 웃음을 주는 농담, 퀴즈, 밈 등을 상황에 맞게 유쾌하게 전달해 주세요.
    """

# API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
if not openai_api_key:
    st.info("API 키를 입력해 주세요.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # 인사말 & 예시 질문
    greetings = [
        "🌱 지구를 아끼는 당신, 오늘도 배꼽은 챙기셨나요?\n♻️ 웃음은 무한 재생 가능 자원이에요!\n😄 지금부터 탄소 대신 개그를 배출합니다!",
        "🌍 환영합니다! 지구를 위한 작은 미소, 여기서 시작돼요.\n🚲 오늘도 배꼽봇과 함께 웃음 탄소중립 도전!\n😆 '지구야 미안해~ 나 오늘 또 웃을 거야!'",
        "🌿 자연은 숨 쉬고, 당신은 웃고, 배꼽봇은 개그해요!\n🌸 친환경 유머, 감성 재생 중입니다.\n🤣 오늘 하루 지구도 웃을 거예요."
    ]
    example_questions = [
        "재밌는 퀴즈 하나 줘! 🤔",
        "요즘 제일 핫한 밈 알려줘 🔥",
        "아재개그 하나만 부탁해요 😂",
        "기분 안 좋을 때 들으면 좋은 유머 있어?",
        "세계에서 제일 웃긴 농담 알려줘!"
    ]

    # 세션 상태 초기화
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.session_state.saved_jokes = []
        st.session_state.style_scores = {"dad_joke": 0, "nonsense": 0, "dark": 0}
        st.session_state.greeted = False
        st.session_state.response_saved = False

    # 초기 환영 메시지 & 예시 말풍선
    if not st.session_state.greeted:
        with st.chat_message("assistant"):
            st.markdown(random.choice(greetings))
        st.markdown("#### 💬 이런 질문 해볼까요?")
        for i, q in enumerate(example_questions):
            if st.button(f"💭 {q}", key=f"btn{i}"):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.greeted = True
                st.rerun()  # ✅ 최신 Streamlit용 (1.27+)

    # 사이드바
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

        # 유머 취향 점수 그래프
        fig, ax = plt.subplots()
        ax.bar(st.session_state.style_scores.keys(), st.session_state.style_scores.values(), color=["#f1c40f", "#2ecc71", "#e74c3c"])
        ax.set_title("유머 취향 점수")
        st.pyplot(fig)

    # 이전 메시지 출력
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    if prompt := st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 수동 스트리밍
        full_response = ""
        with st.chat_message("assistant"):
            with st.spinner("배꼽 터지는 중... 🤣"):
                stream = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    stream=True
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.get("content", "")
                    full_response += content
                    st.markdown(content)

            # 저장 버튼 (1회만)
            if not st.session_state.response_saved and st.button("⭐ 이 유머 저장하기"):
                st.session_state.saved_jokes.append(full_response)
                st.session_state.response_saved = True

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("😂 아재개그 스타일!"):
                    st.session_state.style_scores["dad_joke"] += 1
            with col2:
                if st.button("😶 넌센스 같아요"):
                    st.session_state.style_scores["nonsense"] += 1
            with col3:
                if st.button("😈 블랙유머 느낌"):
                    st.session_state.style_scores["dark"] += 1

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.response_saved = False  # 다음 응답을 위해 리셋
