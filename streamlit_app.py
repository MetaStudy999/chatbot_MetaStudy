import streamlit as st
import random
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="😂 배꼽봇", page_icon="😜")
st.title("😂 배꼽봇 (BaekkopBot)")

# 상단 설명
st.markdown("""
**“당신을 웃게 만드는 단 한 명의 개그 친구, 배꼽봇!”**<br>
피곤한 하루에 한 줄의 농담, 스트레스를 날려줄 찐친 유머 챗봇! 😆\n

당신의 연령, 말투, 취향에 맞춘 ‘맞춤형 웃음 처방’으로 하루를 새롭게 시작하세요.<br>
기분 안 좋을 땐? “배꼽봇, 나 좀 웃겨줘!” 한마디면 OK!\n

API 키를 입력하고 한 줄 웃음 충전 시작해보세요!

---

🔑 [OpenAI API Key](https://platform.openai.com/account/api-keys)를 입력하세요.
""")

# API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 시스템 프롬프트: 배꼽봇 성격 설정
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

    # 세션 상태 초기화 및 무작위 환경 유머 인사
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

        greetings = [
            "🌱 지구를 아끼는 당신, 오늘도 배꼽은 챙기셨나요?\n♻️ 웃음은 무한 재생 가능 자원이에요!\n😄 지금부터 탄소 대신 개그를 배출합니다!",
            "🌍 환영합니다! 지구를 위한 작은 미소, 여기서 시작돼요.\n🚲 오늘도 배꼽봇과 함께 웃음 탄소중립 도전!\n😆 '지구야 미안해~ 나 오늘 또 웃을 거야!'",
            "🌿 자연은 숨 쉬고, 당신은 웃고, 배꼽봇은 개그해요!\n🌸 친환경 유머, 감성 재생 중입니다.\n🤣 오늘 하루 지구도 웃을 거예요.",
            "🌳 종이 대신 웃음으로 마음을 채워볼까요?\n🌞 친환경 유머봇 배꼽봇이 오늘도 출근했습니다!\n😜 웃음은 나누면 지구도 행복해집니다.",
            "🍃 탄소보다 가벼운 웃음이 필요하신가요?\n🌈 배꼽봇이 오늘도 지구를 구할 개그 장전 완료!\n😄 지금부터 본격 친환경 농담 타임 시작합니다!"
        ]

        welcome_msg = random.choice(greetings)
        with st.chat_message("assistant"):
            st.markdown(welcome_msg)

    # 이전 메시지 출력
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
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
