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
    
    selected_age = st.selectbox(
        "당신의 연령대를 선택해 주세요 😊",
        list(age_greetings.keys()),
        key="age_group"
    )

    openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")

# GPT 연결
if not openai_api_key:
    st.info("사이드바에서 OpenAI API 키를 입력해 주세요.", icon="🗝️")
    st.stop()
client = OpenAI(api_key=openai_api_key)

# 시스템 메시지 반영
if "messages" not in st.session_state:
    st.session_state.messages = []

system_msg = {
    "role": "system",
    "content": f"사용자의 연령대는 '{selected_age}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."
}
if st.session_state.messages:
    if st.session_state.messages[0]["role"] == "system":
        st.session_state.messages[0] = system_msg
    else:
        st.session_state.messages.insert(0, system_msg)
else:
    st.session_state.messages = [system_msg]

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 연령대 안내 및 유머 버튼 출력
st.markdown(f"👉 선택한 연령대: **{selected_age}**")
st.markdown("#### 🎯 유머 소개 문구 중 하나를 눌러보세요:")

for msg in age_greetings[selected_age]:
    if st.button(msg):
        st.session_state.messages.append({"role": "user", "content": msg})
        with st.chat_message("user"):
            st.markdown(msg)

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 사용자 입력창
if prompt := st.chat_input("웃음이 필요할 땐? 여기에 써 보세요! 😆"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
