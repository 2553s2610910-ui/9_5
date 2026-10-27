import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="최신 신조어 백과사전 & 퀴즈", page_icon="🔥", layout="centered")

# 2. 신조어 데이터
DATA = [
    {
        "word": "줴줴이야",
        "meaning": "주짓수를 귀엽거나 장난스럽게 부르는 신조어 표현",
        "detail": "주짓수(Jiujitsu)의 발음을 밈 형태로 유머러스하게 변형한 말입니다.",
        "example": "오늘 운동으로 줴줴이야 하러 갈 사람 구함!",
        "options": ["주짓수를 부르는 신조어", "음식이 맛있을 때 내는 소리", "당황했을 때 외치는 말", "게임 승리 포즈"],
        "answer": 0
    },
    {
        "word": "엄....",
        "meaning": "말문이 막히거나 상황이 어색할 때 길게 끄는 감탄사",
        "detail": "선뜻 답하기 힘들거나 곤란한 질문을 받았을 때 어색한 침묵을 표현합니다.",
        "example": "A: 나 오늘 옷 어때? B: 엄....",
        "options": ["화가 났을 때 내는 소리", "어색하거나 말문이 막힐 때 쓰는 표현", "엄마를 부르는 신조어", "매우 만족했을 때 표정"],
        "answer": 1
    },
    {
        "word": "L을 가져가!!!!!!!",
        "meaning": "상대방에게 패배(Loss/L)를 안겨주며 놀리는 밈",
        "detail": "영단어 Loss(패배)의 앞 글자 L에서 유래하여 '너 패배나 먹어라!'라는 뜻으로 쓰입니다.",
        "example": "이번 대결은 나의 완승! 너는 그냥 L을 가져가!!!!!!!",
        "options": ["사랑(Love)을 전하는 말", "상대에게 패배(Loss)를 안겨줄 때 쓰는 밈", "행운(Luck)을 빌어주는 유행어", "퇴근(Leave)할 때 하는 인사"],
        "answer": 1
    },
    {
        "word": "글로벌 유튜버! 원더재빈!",
        "meaning": "특정 크리에이터의 중독성 있는 자기소개 캐치프레이즈",
        "detail": "특유의 텐션과 억양으로 숏폼 플랫폼 등에서 유행하는 밈 구호입니다.",
        "example": "안녕하세요! 텐션 올려~ 글로벌 유튜버! 원더재빈!",
        "options": ["외국인 전용 앱 이름", "중독성 있는 자기소개 밈 구호", "유튜브 시청 꿀팁", "신종 자격증 이름"],
        "answer": 1
    },
    {
        "word": "야르렁",
        "meaning": "'야르'에 '으르렁'을 더해 기분과 흥을 과장되게 표현하는 말",
        "detail": "신나는 마음이나 기세를 강하게 드러낼 때 쓰는 감탄사입니다.",
        "example": "오늘 마침내 금요일이다! 야르렁~!",
        "options": ["강아지가 짖는 소리", "신남과 흥을 기세 있게 표현하는 감탄사", "야간 자율학습 줄임말", "슬플 때 내는 소리"],
        "answer": 1
    },
    {
        "word": "야르",
        "meaning": "'야호'나 '나이스'처럼 기쁨을 나타내는 환호 추임새",
        "detail": "오랫동안 쓰여온 추임새로 최근 숏폼 콘텐츠에서 다시 유행하고 있습니다.",
        "example": "칼퇴 성공했다! 야르!",
        "options": ["기쁨과 환호를 나타내는 추임새", "야구장에 갈 때 쓰는 말", "야식 먹자는 요청", "약속 어겼을 때 사과"],
        "answer": 0
    },
    {
        "word": "한정선",
        "meaning": "과일 찹쌀떡으로 대유행 중인 트렌디한 디저트 핫플 브랜드",
        "detail": "성수동 등에서 줄 서서 먹는 과일 찹쌀떡으로 유명한 디저트 밈입니다.",
        "example": "주말에 줄 서서 한정선 사 먹고 왔어!",
        "options": ["지하철 노선 이름", "유명 과일 찹쌀떡 디저트 브랜드", "한정판 선물 줄임말", "조선시대 경계선"],
        "answer": 1
    },
    {
        "word": "고디바",
        "meaning": "고급 초콜릿 브랜드이자, '달콤함/고급스러움'을 뜻하는 밈",
        "detail": "찐한 달콤함이나 고품격 디저트를 빗대어 부를 때 쓰입니다.",
        "example": "오늘 먹은 디저트 완전 고디바 그 자체인데?",
        "options": ["고구마 디저트 바", "고급 초콜릿 브랜드 및 달콤함을 뜻하는 밈", "고등학생 디지털 바인더", "고전 바지 이름"],
        "answer": 1
    }
]

# 3. 세션 변수 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "step" not in st.session_state:
    st.session_state.step = 0
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

# 4. 앱 헤더
st.title("🔥 최신 신조어 백과사전 & 퀴즈")
st.caption("요즘 인스타, 틱톡, 숏폼을 점령한 신조어를 한눈에 모아보세요!")

tab1, tab2 = st.tabs(["🎯 신조어 퀴즈", "📚 백과사전"])

# [탭 1] 퀴즈
with tab1:
    st.subheader("내가 바로 밈 박사? 퀴즈 풀어보기")

    if st.session_state.quiz_done:
        st.balloons()
        st.success(f"🎉 퀴즈 종료! 결과: **{len(DATA)}문제 중 {st.session_state.score}점**")
        
        if st.session_state.score == len(DATA):
            st.info("🏆 **당신은 'Z세대 밈 전문가'!** 모든 신조어를 완벽하게 파악하고 계시네요!")
        else:
            st.info("😎 **다시 도전해보세요!** 백과사전 탭에서 공부하면 만점을 받을 수 있습니다.")

        if st.button("🔄 처음부터 다시 풀기"):
            st.session_state.score = 0
            st.session_state.step = 0
            st.session_state.quiz_done = False
            st.rerun()

    else:
        idx = st.session_state.step
        item = DATA[idx]

        st.progress((idx) / len(DATA))
        st.markdown(f"#### **Q{idx+1}. '{item['word']}'의 뜻으로 올바른 것은?**")

        # Form을 사용하여 제출 시 동작을 깔끔하게 처리
        with st.form(key=f"quiz_form_{idx}"):
            user_choice = st.radio(
                "하나를 선택하세요:",
                options=list(range(len(item["options"]))),
                format_func=lambda x: item["options"][x]
            )
            submit = st.form_submit_button("정답 제출")

            if submit:
                if user_choice == item["answer"]:
                    st.session_state.score += 1
                    st.toast("정답입니다! 👏", icon="✅")
                else:
                    st.toast("아쉽네요! 오답입니다.", icon="❌")

                if idx + 1 < len(DATA):
                    st.session_state.step += 1
                else:
                    st.session_state.quiz_done = True
                st.rerun()

# [탭 2] 백과사전
with tab2:
    st.subheader("📚 최신 신조어 모아보기")
    
    search = st.text_input("🔍 궁금한 신조어 검색", "")
    
    for item in DATA:
        if search.lower() in item["word"].lower() or search.lower() in item["meaning"].lower():
            with st.expander(f"📌 **{item['word']}**"):
                st.write(f"**의미:** {item['meaning']}")
                st.write(f"**설명:** {item['detail']}")
                st.info(f"**활용 예시:** \"{item['example']}\"")

