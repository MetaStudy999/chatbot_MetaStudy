import streamlit as st
from openai import OpenAI

# 연령대별 유머 안내 메시지
age_greetings = {
    "10대 이하": [
        "안녕! 장난꾸러기 친구 왔네~ 혹시 똥 얘기도 좋아해? 😆",
        "게임 좋아하지? 배꼽봇은 개그로 레벨업 시켜줄게!",
        "엄마 몰래 웃긴 이야기 듣고 싶어? 그럼 조용히 따라와~ 🤫",
        "웃긴 동물 얘기 해줄까? 아님 선생님 놀리는 유머?"
    ],
    "청년 (20~30대)": [
        "자취하는데 배달보다 비싼 건 바로 내 눈물… 웃음으로 위로해줄게!",
        "면접, 연애, 친구… 스트레스 폭발? 개그로 해결하자!",
        "요즘 짤처럼 짧고 강한 웃음, 준비됐어?",
        "헬창이든 넷플릭스 폐인이든, 웃음은 공평해야지~"
    ],
    "중년 (40~50대)": [
        "애 키우느라 웃을 시간 없었죠? 지금 딱 5초만 빵 터져봐요!",
        "부장님 농담 지겹죠? 진짜 재밌는 건 따로 있어요!",
        "월급날보다 반가운 유머, 오늘도 한 줄 드릴게요.",
        "등골 휘는 인생 속 한줄기 웃음, 제가 책임집니다!"
    ],
    "장년 (60대)": [
        "요즘 개그는 뭔지 잘 모르겠다고요? 제가 쉽게 풀어드릴게요~",
        "손주들한테 웃긴 얘기 해주고 싶으시죠? 준비됐어요!",
        "웃음이 건강의 비결이래요. 배꼽봇과 매일 한 줄 유머 어때요?",
        "그 시절 개그 감성도 OK, 요즘 감성도 OK!"
    ],
    "노년 (70대 이상)": [
        "할아버지, 할머니도 웃어야 젊어집니다! 개그 타임~ 😄",
        "옛날 유머도 좋지만, 요즘 세상도 재밌는 게 많답니다!",
        "이런 개그는 처음이지? 부담 없이 웃고 가세요~",
        "건강한 하루, 웃음 한 줄부터 시작해요!"
    ]
}

# 페이지 설정 및 로고
st.set_page_config(page_title="배꼽봇 😂", page_icon="😂")
st.image("logo.png", width=700)

st.title("😂 배꼽봇 (BaekkopBot)")

# 👉 사이드바 구성
with st.sidebar:
    st.header("🧭 설정")
    
    # 연령대 선택
    selected_age = st.selectbox(
        "당신의 연령대를 선택해 주세요 😊",
        list(age_greetings.keys()),
        key="age_group"
    )

    # API 키 입력
    openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")

# 연령대 안내 및 맞춤 메시지 출력
st.markdown(f"👉 선택한 연령대: **{st.session_state.age_group}**")
for msg in age_greetings[st.session_state.age_group]:
    st.markdown(f"- {msg}")

st.markdown("""
**“당신을 웃게 만드는 단 한 명의 개그 친구, 배꼽봇!”**  
피곤한 하루에 한 줄의 농담, 스트레스를 날려줄 찐친 유머 챗봇!  
당신의 연령, 말투, 취향에 맞춘 ‘맞춤형 웃음 처방’으로 하루를 새롭게 시작하세요.  
기분 안 좋을 땐? **“배꼽봇, 나 좀 웃겨줘!”** 한마디면 OK!

---

💡 이 앱은 OpenAI GPT-4o 모델을 기반으로 작동하며, 유머 콘텐츠를 생성합니다.  
🔑 사용을 위해 왼쪽 사이드바에서 API 키를 입력해 주세요.
""")

# GPT 기능 시작
if not openai_api_key:
    st.info("사이드바에서 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 시스템 메시지 항상 최신 연령대 반영
    system_msg = {
        "role": "system",
        "content": f"사용자의 연령대는 '{st.session_state.age_group}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."
    }

    if st.session_state.messages:
        if st.session_state.messages[0]["role"] == "system":
            st.session_state.messages[0] = system_msg
        else:
            st.session_state.messages.insert(0, system_msg)
    else:
        st.session_state.messages = [system_msg]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 입력창 처리
    if prompt := st.chat_input("웃음이 필요할 땐? 여기에 써 보세요! 😆"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성 및 출력
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
