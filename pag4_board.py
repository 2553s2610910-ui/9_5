
import random
import streamlit as st

st.set_page_config(
    page_title="요즘말 사전",
    page_icon="📚",
    layout="wide",
)

# -------------------------
# 기본 신조어 데이터
# -------------------------
DEFAULT_WORDS = [
    {
        "word": "야르",
        "category": "유행 표현",
        "meaning": "기분이 좋거나 신나는 상황에서 사용하는 감탄 표현.",
        "example": "오늘 급식 완전 맛있다, 야르!",
        "description": "즐거움이나 만족감을 표현할 때 쓸 수 있어요. 사용되는 상황에 따라 의미가 달라질 수 있어요.",
        "keywords": "신남 기쁨 감탄",
    },
    {
        "word": "늙크크",
        "category": "유행 표현",
        "meaning": "온라인에서 나이와 관련된 장난이나 밈으로 사용되는 표현.",
        "example": "이 표현은 늙크크 느낌인데?",
        "description": "사용하는 커뮤니티나 유행에 따라 뜻이 달라질 수 있는 표현이에요. 정확한 의미는 대화 맥락을 확인해 보세요.",
        "keywords": "나이 밈 인터넷 유행",
    },
    {
        "word": "영크크",
        "category": "유행 표현",
        "meaning": "온라인에서 젊은 세대나 나이와 관련된 장난으로 쓰일 수 있는 표현.",
        "example": "이런 말투는 영크크 같아!",
        "description": "정해진 표준 의미가 널리 확립된 단어는 아니므로, 실제 대화에서 어떤 뜻으로 쓰였는지 확인하는 것이 좋아요.",
        "keywords": "젊음 세대 밈 인터넷",
    },
    {
        "word": "L을 가져가",
        "category": "인터넷 밈",
        "meaning": "패배나 실패를 받아들이라는 의미로 쓰이는 표현.",
        "example": "이번 대결은 내가 졌네. L을 가져가!",
        "description": "영어 인터넷 표현인 'take the L'과 관련 있어요. 여기서 L은 loss(패배)를 뜻해요.",
        "keywords": "패배 실패 게임 영어 밈",
    },
    {
        "word": "감옥에서 누가 돌아왔게",
        "category": "인터넷 밈",
        "meaning": "누군가 다시 나타난 상황을 과장해서 표현하는 말.",
        "example": "며칠 동안 안 보이던 친구가 왔어. 감옥에서 누가 돌아왔게!",
        "description": "밈이나 특정 영상에서 유래했을 수 있는 표현이에요. 원본 콘텐츠와 대화 맥락에 따라 의미가 달라질 수 있어요.",
        "keywords": "복귀 등장 재등장 유행어",
    },
    {
        "word": "억까",
        "category": "감정 표현",
        "meaning": "억지로 까내리기의 줄임말.",
        "example": "잘못한 것도 없는데 억까하지 마!",
        "description": "정당한 이유 없이 누군가를 비난하거나 불리하게 평가하는 상황에서 사용해요.",
        "keywords": "비난 억지 불공정",
    },
    {
        "word": "알잘딱깔센",
        "category": "줄임말",
        "meaning": "알아서 잘, 딱, 깔끔하고 센스 있게의 줄임말.",
        "example": "자료 정리 알잘딱깔센으로 부탁해!",
        "description": "일일이 설명하지 않아도 상황에 맞게 센스 있게 처리해 달라는 뜻이에요.",
        "keywords": "센스 일 처리 줄임말",
    },
    {
        "word": "킹받네",
        "category": "감정 표현",
        "meaning": "매우 열받거나 짜증 난다는 뜻의 유행 표현.",
        "example": "게임에서 계속 지니까 킹받네!",
        "description": "화가 나거나 약이 오르는 상황에서 장난스럽게 쓰기도 해요.",
        "keywords": "짜증 화남 감정",
    },
    {
        "word": "스불재",
        "category": "줄임말",
        "meaning": "스스로 불러온 재앙의 줄임말.",
        "example": "시험 전날까지 놀다가 밤새 공부라니 스불재다.",
        "description": "자신의 행동 때문에 좋지 않은 결과가 생겼을 때 사용해요.",
        "keywords": "후회 결과 행동",
    },
    {
        "word": "폼 미쳤다",
        "category": "감정 표현",
        "meaning": "실력이나 상태가 매우 뛰어나다는 뜻.",
        "example": "오늘 경기 폼 미쳤다!",
        "description": "누군가의 실력, 외모, 활약 등이 눈에 띄게 좋을 때 칭찬하는 표현이에요.",
        "keywords": "칭찬 실력 멋짐",
    },
    {
        "word": "도파민",
        "category": "유행 표현",
        "meaning": "재미있거나 자극적인 콘텐츠에서 즐거움과 기대감을 느끼는 것을 비유하는 말.",
        "example": "반전이 계속 나와서 도파민 터진다!",
        "description": "일상 대화에서는 재미와 흥미가 강한 상황을 표현할 때 자주 사용해요. 실제 뇌의 도파민 작용과 인터넷에서의 비유적 사용은 구별해야 해요.",
        "keywords": "재미 자극 흥미 콘텐츠",
    },
    {
        "word": "TMI",
        "category": "줄임말",
        "meaning": "Too Much Information의 줄임말로, 지나치게 자세하거나 불필요한 정보라는 뜻.",
        "example": "오늘 아침에 뭘 먹었는지까지 알려주는 건 TMI야!",
        "description": "굳이 알 필요가 없는 사소한 정보를 말할 때 사용해요.",
        "keywords": "정보 영어 줄임말",
    },
]


if "custom_words" not in st.session_state:
    st.session_state.custom_words = []

if "random_word" not in st.session_state:
    st.session_state.random_word = None


def get_words():
    """기본 단어와 직접 등록한 단어를 합쳐 반환합니다."""
    combined = DEFAULT_WORDS + st.session_state.custom_words
    unique = {}

    for item in combined:
        unique[item["word"].strip().lower()] = item

    return list(unique.values())


def show_word(item):
    """신조어의 뜻과 사용 예시를 표시합니다."""
    st.subheader(f"💬 {item['word']}")
    st.caption(f"분류: {item['category']}")
    st.markdown("**📖 뜻**")
    st.write(item["meaning"])
    st.markdown("**🗣️ 사용 예시**")
    st.info(item["example"])
    st.markdown("**💡 쉽게 이해하기**")
    st.write(item["description"])


# -------------------------
# 화면 디자인
# -------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #237B52;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #777777;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">📚 요즘말 사전</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">모르는 신조어, 이제 쉽게 찾아보자!</div>',
    unsafe_allow_html=True,
)

st.divider()

# -------------------------
# 메뉴
# -------------------------
menu = st.radio(
    "메뉴 선택",
    ["🔎 신조어 검색", "🎲 랜덤 신조어", "✍️ 신조어 등록"],
    horizontal=True,
    label_visibility="collapsed",
)

words = get_words()

# -------------------------
# 1. 신조어 검색
# -------------------------
if menu == "🔎 신조어 검색":
    st.header("🔎 신조어 검색")
    st.write("단어 또는 뜻을 입력해 신조어를 찾아보세요.")

    query = st.text_input(
        "검색어",
        placeholder="예: 야르, 억까, 패배, 칭찬",
    )

    categories = ["전체"] + sorted(
        {item["category"] for item in words}
    )

    category = st.selectbox("분류 선택", categories)

    filtered = []
    for item in words:
        searchable = " ".join([
            item["word"],
            item["meaning"],
            item["example"],
            item["description"],
            item["keywords"],
            item["category"],
        ]).lower()

        matches_query = query.strip().lower() in searchable
        matches_category = (
            category == "전체" or item["category"] == category
        )

        if matches_query and matches_category:
            filtered.append(item)

    st.caption(f"검색 결과: {len(filtered)}개")

    if not filtered:
        st.warning("검색 결과가 없어요. 다른 단어로 검색해 보세요.")
    else:
        for index, item in enumerate(filtered):
            with st.expander(f"📌 {item['word']}"):
                show_word(item)

# -------------------------
# 2. 랜덤 신조어
# -------------------------
elif menu == "🎲 랜덤 신조어":
    st.header("🎲 오늘의 랜덤 신조어")
    st.write("버튼을 눌러 새로운 신조어를 알아보세요!")

    if st.button("✨ 신조어 뽑기", type="primary"):
        st.session_state.random_word = random.choice(words)["word"]

    if st.session_state.random_word:
        selected = next(
            (
                item for item in words
                if item["word"] == st.session_state.random_word
            ),
            None,
        )

        if selected:
            show_word(selected)
        else:
            st.info("단어 목록이 바뀌었어요. 다시 뽑아 주세요.")
    else:
        st.info("아직 뽑은 단어가 없어요. 버튼을 눌러 보세요!")

# -------------------------
# 3. 신조어 직접 등록
# -------------------------
elif menu == "✍️ 신조어 등록":
    st.header("✍️ 나만의 신조어 등록")
    st.write("사전에 없는 신조어를 직접 추가할 수 있어요.")

    with st.form("add_word_form", clear_on_submit=True):
        new_word = st.text_input(
            "신조어",
            placeholder="예: 내가 발견한 신조어",
        )
        new_category = st.selectbox(
            "분류",
            ["유행 표현", "인터넷 밈", "줄임말", "감정 표현", "기타"],
        )
        new_meaning = st.text_area("뜻")
        new_example = st.text_input(
            "사용 예시",
            placeholder="예: 이 단어는 이런 상황에서 써요.",
        )
        new_description = st.text_area("쉽게 이해하기")

        submitted = st.form_submit_button("📚 사전에 추가")

    if submitted:
        if not all([
            new_word.strip(),
            new_meaning.strip(),
            new_example.strip(),
            new_description.strip(),
        ]):
            st.error("모든 항목을 입력해 주세요.")
        else:
            existing = {
                item["word"].strip().lower()
                for item in get_words()
            }

            if new_word.strip().lower() in existing:
                st.warning("이미 등록된 단어예요. 다른 이름을 입력해 주세요.")
            else:
                st.session_state.custom_words.append({
                    "word": new_word.strip(),
                    "category": new_category,
                    "meaning": new_meaning.strip(),
                    "example": new_example.strip(),
                    "description": new_description.strip(),
                    "keywords": "",
                })
                st.success(f"'{new_word.strip()}' 단어를 추가했어요!")
                st.rerun()

    st.divider()
    st.subheader("📖 직접 등록한 단어")

    if st.session_state.custom_words:
        for item in st.session_state.custom_words:
            with st.expander(item["word"]):
                show_word(item)
    else:
        st.caption("아직 직접 등록한 단어가 없어요.")

# -------------------------
# 하단 안내
# -------------------------
st.divider()
st.caption(
    f"📚 현재 사전 단어 수: {len(get_words())}개"
)
st.caption(
    "신조어는 커뮤니티와 상황에 따라 의미가 달라질 수 있어요. "
    "특히 유행 밈은 원본 맥락을 함께 확인해 주세요."
)

