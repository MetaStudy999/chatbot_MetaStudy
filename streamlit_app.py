# 사이드바 구성
with st.sidebar:
    st.header("🧭 설정")
    
    # 연령대 선택 (변경 즉시 반영)
    selected_age = st.selectbox(
        "당신의 연령대를 선택해 주세요 😊",
        ["10대 이하", "청년 (20~30대)", "중년 (40~50대)", "장년 (60대)", "노년 (70대 이상)"],
        key="age_group"
    )

    # API 키 입력
    openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")

# 연령대 안내
st.markdown(f"👉 선택한 연령대: **{st.session_state.age_group}**")

# GPT 기능 시작
if not openai_api_key:
    st.info("사이드바에서 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 시스템 메시지 업데이트 (항상 최신 연령대 반영)
    # 첫 메시지가 system이면 덮어쓰기, 아니면 추가
    if st.session_state.messages:
        if st.session_state.messages[0]["role"] == "system":
            st.session_state.messages[0]["content"] = f"사용자의 연령대는 '{st.session_state.age_group}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."
        else:
            st.session_state.messages.insert(0, {
                "role": "system",
                "content": f"사용자의 연령대는 '{st.session_state.age_group}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."
            })
    else:
        st.session_state.messages = [{
            "role": "system",
            "content": f"사용자의 연령대는 '{st.session_state.age_group}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."
        }]
