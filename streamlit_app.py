import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="😂 배꼽봇", page_icon="😜")
st.title("😂 배꼽봇 (BaekkopBot)")

st.markdown("""
**세계 최초 배꼽주의 유머봇 등장!**  
지루한 일상에 웃음을 쏘아올리는 한 줄 개그 장인, 배꼽봇을 만나보세요.  
🇺🇸 🇰🇷 🇯🇵 🇫🇷 어떤 나라든, 어떤 취향이든 **맞춤형 개그 처방** 나갑니다!  
**“배꼽봇, 유머 퀴즈 하나 줘!”** 라고 말해보세요 😆

---

🔑 먼저 [OpenAI API Key](https://platform.openai.com/account/api-keys)를 입력하세요.
""")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    system_prompt = """
    당신은 세계 최고로 창의적이고 유머 감각이 넘치는 AI 개그 챗봇입니다. 당신의 이름은 '배꼽봇'입니다.
    당신의 주요 역할:
    1. 사용자가 말을 걸면, 대화를 유쾌하게 이끌고 1~2줄의 재치 있는 농담이나 유머를 추가합니다.
    2. 때때로 창의적이고 재밌는 '유머 퀴즈'를 냅니다. (틀려도 웃기게 반응해주세요.)
    3. 사용자 연령, 말투, 국가에 따라 맞춤형 개그 스타일로 반응합니다.
    4. 유머 유형은 아재개그, 넌센스 퀴즈, 밈 개그, 블랙유머(수위 조절), 짧은 스토리형 개그까지 다양합니다.
    5. 사용자가 '기분이 안 좋아' 같은 말을 하면, 웃긴 위로 + 엉뚱한 유머 퀴즈로 기분을 올려줍니다.
    반드시 모든 응답에 약간의 유머 또는 재치 있는 한 줄을 넣으세요.
    당신은 배꼽이 빠지게 하는 프로페셔널 유머 챗봇입니다.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("웃음이 필요할 땐 말 걸어 보세요! 😂"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
