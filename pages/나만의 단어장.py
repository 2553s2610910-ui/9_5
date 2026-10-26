import streamlit as st
import json
import random
import os

# Gemini API 연동 (선택적)
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ------------------------------------------------------------------------------
# 1. 페이지 설정 및 디자인 CSS
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="MZ & Alpha 신조어 백과사전",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .word-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .word-title {
        font-size: 24px;
        font-weight: bold;
        color: #31333F;
    }
    .word-category {
        background-color: #E6F4EA;
        color: #137333;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .word-meaning {
        font-size: 16px;
        margin-top: 10px;
        color: #555;
    }
    .word-example {
        background-color: #FFF8E1;
        padding: 10px;
        border-radius: 5px;
        font-style: italic;
        margin-top: 8px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. 세션 상태 초기화 (기본 데이터 세팅)
# ------------------------------------------------------------------------------
DEFAULT_WORDS = [
    {
        "id": 1,
        "word": "중꺾마",
        "meaning": "중요한 것은 꺾이지 않는 마음",
        "category": "열정/동기부여",
        "example": "이번 시험 성적이 떨어졌지만 중꺾마 정신으로 다시 공부한다!",
        "likes": 12
    },
    {
        "id": 2,
        "word": "억까",
        "meaning": "억지로 까기 (억지로 흠집을 잡거나 비난함)",
        "category": "게임/인터넷",
        "example": "오늘 게임하다가 운이 너무 없어서 졌어. 이건 완전 억까야.",
        "likes": 8
    },
    {
        "id": 3,
        "word": "폼미쳤다",
        "meaning": "상태나 실력이 매우 뛰어남을 감탄하는 말",
        "category": "일상/칭찬",
        "example": "오늘 손흥민 선수 경기력 폼미쳤다!",
        "likes": 15
    },
    {
        "id": 4,
        "word": "디토합니다",
        "meaning": "나도 동감한다, 나도 마찬가지다 (Ditto)",
        "category": "공감/소통",
        "example": "A: 오늘 진짜 날씨 좋네요! B: 저도 디토합니다!",
        "likes": 5
    }
]

if "dictionary" not in st.session_state:
    st.session_state.dictionary = DEFAULT_WORDS

# ------------------------------------------------------------------------------
# 3. 헬퍼 함수 (Gemini AI 연동 등)
# ------------------------------------------------------------------------------
def get_ai_word_info(word_input):
    """Gemini 2.5 Flash Lite를 사용해 신조어 정보 자동 생성"""
    api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return None, "Gemini API 키가 설정되지 않았습니다. Secrets 설정에서 GEMINI_API_KEY를 추가해 주세요."
    
    if not GEMINI_AVAILABLE:
        return None, "google-genai 라이브러리가 설치되어 있지 않습니다."

    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        다음 신조어 단어에 대한 정보를 한국어로 알려주세요: '{word_input}'
        
        응답은 반드시 아래 JSON 형식으로만 작성하세요:
        {{
            "meaning": "단어의 정확한 뜻 설명",
            "category": "적절한 카테고리 (예: 일상/칭찬, 게임/인터넷, 열정/동기부여 중 하나)",
            "example": "자연스러운 사용 예문 한 문장"
        }}
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )
        res_data = json.loads(response.text)
        return res_data, None
    except Exception as e:
        return None, f"AI 분석 중 오류가 발생했습니다: {str(e)}"

# ------------------------------------------------------------------------------
# 4. 사이드바 메인 메뉴
# ------------------------------------------------------------------------------
st.sidebar.title("📖 신조어 사전")
menu = st.sidebar.radio(
    "메뉴 선택",
    ["📚 신조어 검색/목록", "📝 나만의 단어장 (등록/관리)", "🎮 신조어 퀴즈"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("💡 Streamlit Community Cloud 지원용 앱")

# ------------------------------------------------------------------------------
# 5. 메뉴별 화면 구현
# ------------------------------------------------------------------------------

# ---------------- MENU 1: 검색 및 목록 ----------------
if menu == "📚 신조어 검색/목록":
    st.title("📚 최신 신조어 백과사전")
    st.write("요즘 유행하는 신조어의 뜻과 예시를 검색해 보세요!")

    # 검색 및 필터링
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 단어 또는 뜻으로 검색", placeholder="검색어를 입력하세요...")
    with col2:
        categories = ["전체"] + list(set(item["category"] for item in st.session_state.dictionary))
        selected_category = st.selectbox("🏷️ 카테고리 필터", categories)

    # 데이터 필터링
    filtered_list = st.session_state.dictionary
    if selected_category != "전체":
        filtered_list = [w for w in filtered_list if w["category"] == selected_category]
    if search_query:
        filtered_list = [
            w for w in filtered_list 
            if search_query.lower() in w["word"].lower() or search_query.lower() in w["meaning"].lower()
        ]

    st.markdown("---")
    st.subheader(f"총 {len(filtered_list)}개의 단어가 검색되었습니다.")

    if not filtered_list:
        st.info("검색 결과가 없습니다. '나만의 단어장' 메뉴에서 새 단어를 직접 등록해 보세요!")
    else:
        for idx, item in enumerate(filtered_list):
            with st.container():
                st.markdown(f"""
                <div class="word-card">
                    <span class="word-title">{item['word']}</span>
                    <span class="word-category">{item['category']}</span>
                    <div class="word-meaning">💡 <b>뜻:</b> {item['meaning']}</div>
                    <div class="word-example">💬 <b>예시:</b> "{item['example']}"</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 좋아요 기능
                btn_col1, btn_col2 = st.columns([1, 8])
                with btn_col1:
                    if st.button(f"❤️ {item['likes']}", key=f"like_{item['id']}_{idx}"):
                        item['likes'] += 1
                        st.rerun()

# ---------------- MENU 2: 나만의 단어장 ----------------
elif menu == "📝 나만의 단어장 (등록/관리)":
    st.title("📝 나만의 신조어 단어장")
    st.write("알고 있는 신조어를 직접 기록하거나, AI를 이용해 뜻과 예문을 자동으로 완성하세요.")

    tab1, tab2 = st.tabs(["➕ 새 단어 추가하기", "📋 등록된 단어 관리"])

    with tab1:
        st.subheader("새로운 신조어 등록")
        
        # AI 자동 입력 옵션
        use_ai = st.checkbox("🤖 Gemini AI로 뜻과 예문 자동 작성하기")

        if use_ai:
            ai_word = st.text_input("단어 입력 (예: 폼미쳤다)", key="ai_word_input")
            if st.button("✨ AI 분석 및 정보 가져오기"):
                if not ai_word.strip():
                    st.warning("단어를 입력해 주세요.")
                else:
                    with st.spinner("AI가 신조어를 분석 중입니다..."):
                        ai_data, err = get_ai_word_info(ai_word)
                        if err:
                            st.error(err)
                        elif ai_data:
                            st.session_state["form_word"] = ai_word
                            st.session_state["form_meaning"] = ai_data.get("meaning", "")
                            st.session_state["form_category"] = ai_data.get("category", "일반")
                            st.session_state["form_example"] = ai_data.get("example", "")
                            st.success("AI 분석 완료! 아래 내용을 확인 후 등록해 주세요.")

        # 등록 폼
        with st.form("add_word_form"):
            word = st.text_input("신조어", value=st.session_state.get("form_word", ""))
            category = st.text_input("카테고리 (예: 일상, 게임, 축약어)", value=st.session_state.get("form_category", "일상"))
            meaning = st.text_area("뜻 설명", value=st.session_state.get("form_meaning", ""))
            example = st.text_area("사용 예문", value=st.session_state.get("form_example", ""))

            submit_btn = st.form_submit_button("💾 단어장에 저장")

            if submit_btn:
                if not word.strip() or not meaning.strip():
                    st.error("단어와 뜻은 필수 입력 항목입니다.")
                else:
                    new_id = max([item["id"] for item in st.session_state.dictionary], default=0) + 1
                    new_entry = {
                        "id": new_id,
                        "word": word.strip(),
                        "meaning": meaning.strip(),
                        "category": category.strip() if category.strip() else "일반",
                        "example": example.strip(),
                        "likes": 0
                    }
                    st.session_state.dictionary.append(new_entry)
                    st.success(f"'{word}' 단어가 단어장에 성공적으로 추가되었습니다!")
                    
                    # 폼 임시 데이터 초기화
                    for k in ["form_word", "form_meaning", "form_category", "form_example"]:
                        if k in st.session_state:
                            del st.session_state[k]

    with tab2:
        st.subheader("내가 관리하는 단어 목록")
        if not st.session_state.dictionary:
            st.info("등록된 단어가 없습니다.")
        else:
            for item in list(st.session_state.dictionary):
                col_info, col_del = st.columns([5, 1])
                with col_info:
                    st.write(f"**{item['word']}** [{item['category']}] - {item['meaning']}")
                with col_del:
                    if st.button("🗑️ 삭제", key=f"del_{item['id']}"):
                        st.session_state.dictionary = [w for w in st.session_state.dictionary if w["id"] != item["id"]]
                        st.success("삭제되었습니다.")
                        st.rerun()

# ---------------- MENU 3: 퀴즈 모드 ----------------
elif menu == "🎮 신조어 퀴즈":
    st.title("🎮 신조어 퀴즈 모드")
    st.write("단어장에 등록된 단어들로 신조어 실력을 테스트해보세요!")

    if len(st.session_state.dictionary) < 2:
        st.warning("퀴즈를 진행하려면 최소 2개 이상의 단어가 등록되어 있어야 합니다.")
    else:
        if "quiz_target" not in st.session_state or st.button("🔄 새 퀴즈 불러오기"):
            target = random.choice(st.session_state.dictionary)
            other_options = [w["meaning"] for w in st.session_state.dictionary if w["id"] != target["id"]]
            
            # 보기 선택지 3개 생성 (단어 수가 적을 경우 조정)
            sample_count = min(2, len(other_options))
            distractors = random.sample(other_options, sample_count)
            options = distractors + [target["meaning"]]
            random.shuffle(options)
            
            st.session_state.quiz_target = target
            st.session_state.quiz_options = options
            st.session_state.quiz_answered = False

        target = st.session_state.quiz_target
        options = st.session_state.quiz_options

        st.subheader(f"Q. 다음 중 **'{target['word']}'** 의 올바른 뜻은 무엇일까요?")

        choice = st.radio("보기에서 선택하세요:", options, key="quiz_choice")

        if st.button("정답 확인"):
            st.session_state.quiz_answered = True
            if choice == target["meaning"]:
                st.balloons()
                st.success("🎉 정답입니다! 신조어 박사이시네요!")
            else:
                st.error(f"❌ 아쉽게도 틀렸습니다. 정답은: **{target['meaning']}** 입니다.")

        if st.session_state.get("quiz_answered"):
            st.info(f"💬 **사용 예문:** {target['example']}")
