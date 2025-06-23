물론이죠! Streamlit에서 왼쪽 네비게이션 창(사이드바)을 만들려면 `st.sidebar`를 사용하면 됩니다. 연령대 선택, API 키 입력 같은 항목을 사이드바로 옮기면 메인 화면이 더 깔끔해집니다.

아래는 사이드바를 적용한 수정 예입니다:

```python
import streamlit as st
from openai import OpenAI

# 페이지 설정 및 로고
st.set_page_config(page_title="배꼽봇 😂", page_icon="😂")
st.image("logo.png", width=700)

st.title("😂 배꼽봇 (BaekkopBot)")

# 👉 사이드바 구성
with st.sidebar:
    st.header("🧭 설정")
    
    # 연령대 선택
    age_group = st.selectbox(
        "당신의 연령대를 선택해 주세요 😊",
        ["청년 (20~30대)", "중년 (40~50대)", "장년 (60대)", "노년 (70대 이상)"]
    )

    # API 키 입력
    openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")

# 연령대 안내
st.markdown(f"👉 선택한 연령대: **{age_group}**")

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
        st.session_state.messages = [
            {"role": "system", "content": f"사용자의 연령대는 '{age_group}'입니다. 이에 맞는 유머 스타일로 응답해 주세요."}
        ]

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
```

이제 왼쪽 사이드바에 연령대와 API 키 입력창이 생기고, 메인 페이지는 유머 인터페이스에 집중할 수 있게 됩니다. 필요한 경우 사이드바에 버튼이나 링크도 추가 가능합니다.
