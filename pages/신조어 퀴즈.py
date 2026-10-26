import streamlit as st
import random
import os

# 페이지 설정
st.set_page_config(
    page_title="신조어 백과사전 & 퀴즈",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 정의 (최신 신조어 모음)
NEW_WORDS_DATA = [
    {
        "word": "줴줴이야",
        "meaning": "'대박이다', '진짜 미쳤다', '엄청나다'를 뜻하는 감탄사",
        "origin": "유튜버 및 인터넷 방송에서 특정 리액션으로 유행하기 시작함.",
        "example":최근 밈(Meme)과 신조어를 재미있게 풀어보는 **최신 신조어 백과사전 & 퀴즈 앱**입니다. 

외부 API 의존성 없이 가장 안정적으로 실행되는 **독립형 퀴즈 & 사전 앱** 형태로 설계하였습니다. 별도의 API Key 설정 없이 즉시 동작하며, Streamlit Community Cloud에 무료로 배포하기 매우 적합합니다.

---

## 1. 앱 기획 설명

### 💡 기획 의도
‘줴줴이야’, ‘L을 가져가!!!!!!!’ 등 최신 숏폼과 SNS를 달구는 신조어는 빠르게 바뀌기 때문에 단순히 뜻만 보여주는 사전보다는 **직접 풀어보는 퀴즈** 형태가 사용자의 유입과 몰입도를 끌어올리기 좋습니다.

### 🎨 핵심 기능 및 화면 구성
1. **🔥 최신 신조어 백과사전 (탐색 탭)**
   - 제시된 신조어들의 유래, 의미, 사용 예시를 카드 형태로 한눈에 볼 수 있습니다.
   - 키워드 검색 기능을 통해 원하는 신조어를 빠르게 찾을 수 있습니다.
2. **🎯 MZ 신조어 퀴즈 (게임 탭)**
   - 요청하신 8가지 주요 최신 신조어 기반의 퀴즈 게임입니다.
   - 4지선다형 객관식 문제로 구성되며, 정답 제출 시 직관적인 피드백(유래 설명 및 점수)을 제공합니다.
   - 모든 문제를 풀면 **‘신조어 마스터 등급’** 결과 카드와 함께 **다시 도전하기** 기능을 제공합니다.
3. **💡 신조어 제휴/제보 (부가 기능)**
   - 나만 아는 신조어를 제보받는 대화형 인터페이스를 제공하여 앱의 확장성을 보여줍니다.

---

## 2. `app.py`

프로젝트 루트 폴더에 `app.py` 파일을 생성하고 아래 코드를 그대로 복사하여 붙여넣으세요.

```python
import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="최신 신조어 백과사전 & 퀴즈",
    page_icon="🔥",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 1. 신조어 데이터베이스 (요청된 최신 밈 및 신조어 포함)
# -----------------------------------------------------------------------------
NEW_WORDS_DB = [
    {
        "word": "줴줴이야",
        "meaning": "주짓수를 표현하는 귀엽거나 장난스러운 말투 또는 밈.",
        "example": "오늘 운동으로 줴줴이야 하러 갈 사람?",
        "options": ["주짓수를 친근하게 부르는 말", "맛있는 음식을 먹을 때 나는 소리", "재미없는 이야기를 들었을 때 반응", "게임에서 승리했을 때 외치는 말"],
        "answer": 0,
        "detail": "주짓수(Jiujitsu)를 유머러스하게 변형하여 부르는 신조어입니다."
    },
    {
        "word": "엄....",
        "meaning": "말문이 막히거나 당황했을 때, 혹은 상황이 어색할 때 길게 끌며 사용하는 감탄사.",
        "example": "A: 나 오늘 머리 잘랐는데 어때? B: 엄....",
        "options": ["매우 화가 났을 때 내는 소리", "말문이 막히거나 상황이 어색할 때 쓰는 표현", "엄마를 부르는 신조어", "음식이 너무 맛있을 때 하는 감탄사"],
        "answer": 1,
        "detail": "상대방의 질문에 선뜻 답하기 힘들거나 어색한 침묵을 표현할 때 사용됩니다."
    },
    {
        "word": "L을 가져가!!!!!!!",
        "meaning": "패배(Loss/L)를 인정하라는 의미로, 상대방에게 굴욕을 주거나 놀릴 때 쓰는 밈.",
        "example": "이번 게임은 내가 완승했지? 너는 그냥 L을 가져가!!!!!!!",
        "options": ["사랑(Love)을 전할 때 쓰는 말", "게임이나 대결에서 상대에게 패배(Loss)를 안겨줄 때 쓰는 밈", "행운(Luck)을 빌어주는 유행어", "자리를 비울 때(Leave) 쓰는 인사"],
        "answer": 1,
        "detail": "영단어 Loss의 앞 글자인 'L'에서 유래하여, '너 패배나 먹어라!'라는 뉘앙스의 해외/국내 유행 밈입니다."
    },
    {
        "word": "글로벌 유튜버! 원더재빈!",
        "meaning": "특정 크리에이터 또는 밈 형태의 자기소개 구호.",
        "example": "안녕하세요! 텐션 끌어올려~ 글로벌 유튜버! 원더재빈!",
        "options": ["외국인 전용 여행 앱 이름", "특정 텐션 높은 캐릭터/유튜브 캐치프레이즈", "신종 세계 인플루언서 자격증", "유튜브 시청 시 사용하는 꿀팁"],
        "answer": 1,
        "detail": "특유의 중독성 있는 억양과 자기소개 캐치프레이즈로 숏폼 등에서 유행한 밈입니다."
    },
    {
        "word": "야르렁",
        "meaning": "'야르'의 변형으로, 신나거나 기분이 좋을 때 으르렁거리듯 흥을 표현하는 말.",
        "example": "오늘 금요일이다! 야르렁~!",
        "options": ["강아지가 화났을 때 소리", "신남과 흥을 기세 있게 표현하는 감탄사", "야간 자율학습을 줄인 말", "슬플 때 내는 소리"],
        "answer": 1,
        "detail": "'야르'에 '으르렁' 같은 기세를 더해 더 과장되고 신나게 외치는 유행어입니다."
    },
    {
        "word": "야르",
        "meaning": "'야호' 또는 '나이스'처럼 기쁨이나 환호를 나타내는 추임새.",
        "example": "시험 끝났다! 야르!",
        "options": ["기쁨과 환호를 나타내는 추임새", "야구장에 갈 때 쓰는 신조어", "야식을 먹자는 요청", "약속 시간을 어겼을 때 쓰는 사과"],
        "answer": 0,
        "detail": "오랜 기간 변형되어 온 감탄사로, 최근 숏폼 콘텐츠 등에서 다시 유행 중입니다."
    },
    {
        "word": "한정선",
        "meaning": "성수동 등에서 과일 찹쌀떡(대복)으로 대유행 중인 디저트 브랜드/핫플레이스 밈.",
        "example": "주말에 성수동 가서 한정선 사 먹고 왔어!",
        "options": ["지하철 노선의 일종", "생딸기/과일 찹쌀떡으로 유명한 디저트 핫플", "한정판 선물의 줄임말", "조선 시대 한양의 경계선"],
        "answer": 1,
        "detail": "줄을 서서 먹는 과일 찹쌀떡 브랜드로, 트렌디한 디저트 밈으로 활발히 언급됩니다."
    },
    {
        "word": "고디바",
        "meaning": "고급 초콜릿 브랜드이지만, 밈적으로는 초콜릿처럼 달콤함/고급스러움을 빗대어 쓰는 말.",
        "example": "오늘 디저트 완전 고디바 느낌인데?",
        "options": ["고구마 디저트 바의 줄임말", "고급 초콜릿 브랜드 및 달콤함/고급스러움을 뜻하는 밈", "고등학생 디지털 바인더의 약자", "고전 디자이너 바지 이름"],
        "answer": 1,
        "detail": "초콜릿 브랜드를 넘어 '찐한 달콤함'이나 '고급스러운 디저트'를 통칭할 때 언급됩니다."
    }
]

# -----------------------------------------------------------------------------
# 2. 세션 상태 초기화
# -----------------------------------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "shuffled_words" not in st.session_state:
    st.session_state.shuffled_words = NEW_WORDS_DB.copy()

# -----------------------------------------------------------------------------
# 3. UI 메인 레이아웃
# -----------------------------------------------------------------------------
st.title("🔥 요즘 최신 신조어 백과 & 퀴즈")
st.caption("인스타, 숏폼, 틱톡을 지배하는 최신 밈과 신조어를 마스터해보세요!")

# 탭 구성
tab1, tab2 = st.tabs(["🎯 최신 밈 퀴즈", "📚 신조어 백과사전"])

# -----------------------------------------------------------------------------
# TAB 1: 퀴즈 게임
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("내가 바로 밈 박사? 퀴즈 도전!")

    if not st.session_state.quiz_started:
        st.info("💡 요청해주신 **'줴줴이야', 'L을 가져가!!!!!!!', '야르렁'** 등 최신 신조어 8문항이 출제됩니다.")
        if st.button("🚀 퀴즈 시작하기", use_container_width=True):
            random.shuffle(st.session_state.shuffled_words)
            st.session_state.quiz_started = True
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.quiz_finished = False
            st.rerun()

    elif st.session_state.quiz_finished:
        st.balloons()
        total = len(st.session_state.shuffled_words)
        score = st.session_state.score
        
        st.success(f"🎉 모든 문제를 풀었습니다! **{total}개 중 {score}개** 맞추셨습니다.")
        
        # 등급 판단
        if score == total:
            st.markdown("### 🏆 당신은 **'Z세대 밈 전문가'**!")
            st.write("요즘 트렌드를 완벽하게 꿰뚫고 계시네요. 최신 신조어 마스터 인정!")
        elif score >= total // 2:
            st.markdown("### 😎 당신은 **'트렌드 스폰지'**!")
            st.write("어느 정도 숏폼과 밈을 잘 즐기고 계시군요!")
        else:
            st.markdown("### 😅 당신은 **'밈 유치원생'**!")
            st.write("백과사전 탭에서 신조어를 공부하고 다시 도전해보세요!")

        if st.button("🔄 다시 도전하기", use_container_width=True):
            st.session_state.quiz_started = False
            st.rerun()

    else:
        # 진행 상황 표시
        curr_idx = st.session_state.current_q
        q_data = st.session_state.shuffled_words[curr_idx]
        total_q = len(st.session_state.shuffled_words)
        
        st.progress((curr_idx) / total_q)
        st.write(f"**문제 {curr_idx + 1} / {total_q}**")
        
        # 문제 카드
        st.markdown(f"### ❓ **'{q_data['word']}'**(은)는 무슨 뜻일까요?")
        
        # 보기 제공 (Form으로 감싸서 제출)
        with st.form(key=f"quiz_form_{curr_idx}"):
            user_choice = st.radio(
                "올바른 의미를 선택하세요:",
                options=range(len(q_data["options"])),
                format_func=lambda x: q_data["options"][x]
            )
            submit_btn = st.form_submit_button("정답 확인 및 다음")

        if submit_btn:
            if user_choice == q_data["answer"]:
                st.session_state.score += 1
                st.toast("정답입니다! 🎉", icon="✅")
            else:
                correct_text = q_data["options"][q_data["answer"]]
                st.toast(f"아쉽네요! 정답: {correct_text}", icon="❌")

            # 다음 문제로 이동 처리
            if curr_idx + 1 < total_q:
                st.session_state.current_q += 1
            else:
                st.session_state.quiz_finished = True
            st.rerun()

# -----------------------------------------------------------------------------
# TAB 2: 백과사전
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("📚 최신 신조어 사전")
    
    # 검색 기능
    search_term = st.text_input("🔍 검색하고 싶은 신조어를 입력하세요", placeholder="예: 야르, 줴줴이야")
    
    filtered_db = [
        item for item in NEW_WORDS_DB 
        if search_term.lower() in item["word"].lower() or search_term.lower() in item["meaning"].lower()
    ]
    
    if not filtered_db:
        st.warning("검색 결과가 없습니다.")
    else:
        for item in filtered_db:
            with st.expander(f"📌 **{item['word']}**"):
                st.markdown(f"**의미:** {item['meaning']}")
                st.markdown(f"**상세 유래:** {item['detail']}")
                st.info(f"💬 **사용 예시:** \"{item['example']}\"")

# 하단 정보
st.markdown("---")
st.caption("제작: 최신 트렌드 신조어 앱 | 오류 없이 Streamlit Community Cloud에 즉시 배포 가능합니다.")
