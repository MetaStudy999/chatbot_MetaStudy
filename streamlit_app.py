import streamlit as st
from openai import OpenAI

# 챗봇 이름 및 설명
st.set_page_config(page_title="배꼽봇 😂", page_icon="😂")
st.title("😂 배꼽봇 (BaekkopBot)")
st.markdown("""
**“당신을 웃게 만드는 단 한 명의 개그 친구, 배꼽봇!”**  
피곤한 하루에 한 줄의 농담, 스트레스를 날려줄 찐친 유머 챗봇!  
당신의 연령, 말투, 취향에 맞춘 ‘맞춤형 웃음 처방’으로 하루를 새롭게 시작하세요.  
기분 안 좋을 땐? **“배꼽봇, 나 좀 웃겨줘!”** 한마디면 OK!

---

💡 이 앱은 OpenAI GPT-4o 모델을 기반으로 작동하며, 유머 콘텐츠를 생성합니다.  
🔑 사용을 위해 [OpenAI API 키](https://platform.openai.com/account/api-keys)를 입력해 주세요.
""")

# API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
