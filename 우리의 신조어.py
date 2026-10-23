import os
import json
import random
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 페이지 기본 설정 & 세련된 CSS 스타일링
# ==========================================
st.set_page_config(
    page_title="말랑말랑 신조어 사전 젤리",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 귀엽고 세련된 파스텔 디자인 CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 메인 배경 및 라운딩 스타일 */
    .stApp {
        background-color: #FAFAFD;
    }
    
    /* 타이틀 카드 스타일 */
    .hero-container {
        background: linear-gradient(135deg, #A8EDEA 0%, #FED6E3 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        color: #2D3748;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #4A5568;
        font-size: 1.1rem;
    }

    /* 카드 스타일 */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 1rem;
        transition: transform 0.2s ease-in-out;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
    }
    
    /* 신조어 태그 스타일 */
    .word-badge {
        display: inline-block;
        background-color: #EBF4FF;
        color: #3182CE;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }

    /* 버튼 스타일 조정 */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #F7FAFC;
    }
</style>
""", unsafe_html=True)

# ==========================================
# 2. 데이터 초기화 (세션 상태 관리)
# ==========================================
DEFAULT_WORDS = [
    {
        "word": "분카소",
        "meaning": "분위기 좋은 카페 소문내기의 줄임말. 감성 있는 카페를 추천하거나 방문할 때 자주 쓰임.",
        "example": "이번 주말에 성수동으로 분카소 가볼 사람?",
        "category": "일상/라이프"
    },
    {
        "word": "추억의 맛",
        "meaning": "과거의 감성을 자극하거나 옛날 느낌이 나는 음식/콘텐츠를 의미함.",
        "example": "이 분식집 떡볶이는 완전 추억의 맛이다!",
        "category": "음식/감성"
    },
    {
        "word": "텍스트 힙",
        "meaning": "글을 읽고 쓰며 지적인 취향을 즐기는 것이 멋지다고 생각하는 트렌드.",
        "example": "요즘 종이책 읽으며 텍스트 힙 실천 중이야.",
        "category": "트렌드"
    },
    {
        "word": "갓생",
        "meaning": "God(신) + 생(生)의 합성어. 하루하루 알차고 부지런하게 살아가는 삶.",
        "example": "오늘부터 아침 6시 운동하고 갓생 살기 시작한다!",
        "category": "갓생/자기계발"
    },
    {
        "word": "디저트 배",
        "meaning": "밥을 배불리 먹어도 디저트를 먹을 배는 따로 남아있다는 재미있는 표현.",
        "example": "배터지게 먹었지만 디저트 배는 따로 있지~",
        "category": "음식/감성"
    }
]

if "dictionary" not in st.session_state:
    st.session_state.dictionary = DEFAULT_WORDS.copy()

if "my_notes" not in st.session_state:
    st.session_state.my_notes = [
        {"word": "너 T야?", "meaning": "감정적인 공감 대신 논리적/이성적으로 반응할 때 농담조로 묻는 말", "date": "2026-10-23"}
    ]

# ==========================================
# 3. AI 클라이언트 초기화 함수
# ==========================================
def get_gemini_response(prompt):
    api_key = None
    # Streamlit Secrets 또는 환경 변수 확인
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]

    if not api_key:
        return "⚠️ API 키가 설정되지 않았습니다. Streamlit Secrets에 `GEMINI_API_KEY`를 등록해주세요."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI 답변을 불러오는 중 오류가 발생했습니다: {str(e)}"

# ==========================================
# 4. 헤더 영역
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🍬 말랑말랑 신조어 사전</div>
    <div class="hero-subtitle">트렌디한 신조어 탐색부터 AI 통역, 나만의 메모장까지 한 번에!</div>
</div>
""", unsafe_html=True)

# ==========================================
# 5. 사이드바 메뉴
# ==========================================
st.sidebar.image("https://img.icons8.com/cute-clipart/128/book.png", width=70)
st.sidebar.title("젤리 메뉴")
menu = st.sidebar.radio(
    "원하는 기능을 선택하세요",
    ["📚 신조어 백과사전", "🤖 AI 신조어 통역기", "📝 나만의 신조어 메모장", "🎮 신조어 퀴즈"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: 모르는 신조어는 AI 통역기에게 바로 물어보세요!")

# ==========================================
# 6. 메뉴별 화면 구현
# ==========================================

# ------------------------------------------
# 메뉴 1: 📚 신조어 백과사전
# ------------------------------------------
if menu == "📚 신조어 백과사전":
    st.subheader("🔍 신조어 검색 및 둘러보기")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.요청하신 주제인 **'신조어 백과사전'**과 필수 기능인 **'나만의 메모장'**, 그리고 **AI 기능(Gemini API)**을 결합하여, 세련되고 귀여운 디자인의 Streamlit 앱을 기획 및 구현했습니다.

---

### 1. 앱 기획 설명

#### 💡 앱 제목: **MZ-Dic : 트렌디한 신조어 백과사전 힙스터**

#### 🎨 디자인 컨셉
- **컬러 팔레트:** 파스텔 핑크(#FFB6C1), 민트(#A8E6CF), 크림 베이지 바탕으로 귀엽고 접근하기 쉬운 세련된 톤앤매너 형성
- **타이포그래피 & 카드 뷰:** 둥글둥글한 라운드 스타일과 그림자 효과(Box-shadow)를 더한 커스텀 CSS 적용

#### 🔑 주요 기능
1. **🔍 신조어 검색 및 검색어 제안:**
   - 기본 탑재된 신조어 DB에서 단어/뜻 검색
   - 사용자가 새로운 단어를 입력하면 AI(Gemini 2.5 Flash-lite)가 실시간으로 **의미, 예문, 꿀팁/주의사항**을 생성
2. **📝 나만의 신조어 메모장 (요청 필수 기능):**
   - 사전이나 AI 분석으로 찾아낸 신조어를 나의 개인 메모장에 즉시 추가
   - 나만의 메모장 탭에서 메모 작성, 삭제, 태그 지정 기능 제공
   - 세션 상태(`st.session_state`)를 활용하여 앱 동작 중 데이터가 유실되지 않도록 관리
3. **🎲 오늘의 신조어 퀴즈 (차별화 기능):**
   - 신조어 감각을 테스트할 수 있는 귀여운 카드 형태의 무작위 퀴즈 기능

---

### 2. `app.py` (완전한 코드)

```python
import streamlit as st
import google.generativeai as genai
import json

# ==========================================
# 1. 페이지 설정 및 커스텀 CSS (귀여운 파스텔 톤)
# ==========================================
st.set_page_config(
    page_title="MZ-Dic | 신조어 백과사전",
    page_icon="📖",
    layout="wide"
)

st.markdown("""
<style>
    /* 메인 배경 및 폰트 설정 */
    .stApp {
        background-color: #FFF9F5;
        color: #333333;
    }
    
    /* 카드 스타일 */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
        margin-bottom: 20px;
        border: 2px solid #FFE4E1;
    }
    
    /* 귀여운 태그 스타일 */
    .tag-badge {
        background-color: #A8E6CF;
        color: #2E7D32;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* 타이틀 강조 */
    .title-text {
        font-family: 'Comic Sans MS', sans-serif;
        color: #FF6B6B;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        text-align: center;
        color: #888888;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 초기 데이터 및 세션 상태 설정
# ==========================================
DEFAULT_WORDS = {
    "분집": {"meaning": "분위기 집착남/집착녀의 줄임말. 특정 장소나 상황의 분위기를 매우 중요하게 생각하는 사람.", "example": "성수동 카페거리 왔는데 완전 분집 감성이다!"},
    "중꺾마": {"meaning": "'중요한 것은 꺾이지 않는 마음'의 줄임말. 어려움 속에서도 포기하지 않는 태도.", "example": "시험 기간이지만 중꺾마 정신으로 버틴다."},
    "알파세대": {"meaning": "2010년 이후에 태어난 세대로, 태어날 때부터 디지털 기기를 접한 디지털 온리 세대.", "example": "요즘 알파세대 유행어는 진짜 따라가기 힘들다."}
}

if "my_notes" not in st.session_state:
    st.session_state.my_notes = [
        {"word": "갓생", "meaning": "신(God) + 인생. 부지런하고 알차게 사는 삶.", "memo": "나도 오늘부터 갓생 살기 1일차!"}
    ]

# ==========================================
# 3. Gemini API 설정 (AI 해석 기능)
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")
model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
    except Exception as e:
        st.sidebar.error(f"Gemini API 연결 오류: {e}")

# ==========================================
# 4. 메인 화면 헤더
# ==========================================
st.markdown("<div class='title-text'>📖 MZ-Dic 신조어 백과사전</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>요즘 대세 신조어 검색부터 나만의 단어장 메모까지 한 번에! ✨</div>", unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3 = st.tabs(["🔍 신조어 검색 & AI 분석", "📝 나만의 메모장", "🎲 오늘의 퀴즈"])

# ==========================================
# 탭 1: 신조어 검색 & AI 분석
# ==========================================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔎 신조어 검색하기")
        search_query = st.text_input("궁금한 신조어를 입력하세요 (예: 폼미쳤다, 갓생)", placeholder="단어 입력...")
        
        if search_query:
            # 1차: 기본 DB 검색
            if search_query in DEFAULT_WORDS:
                word_info = DEFAULT_WORDS[search_query]
                st.markdown(f"""
                <div class='custom-card'>
                    <span class='tag-badge'>사전 등록 단어</span>
                    <h3>✨ {search_query}</h3>
                    <p><b>의미:</b> {word
