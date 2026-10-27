import streamlit as st
import datetime
import random

# ==========================================
# 1. Page Configuration & Gemini Style CSS
# ==========================================
st.set_page_config(
    page_title="신조어 백과사전 | Neologism Dictionary",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Gemini-inspired Blue & Dark Blue Palette
st.markdown("""
<style>
    /* Global Fonts & Background Accent */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }

    /* Primary Background & Main Accent Palette */
    :root {
        --gemini-deep-blue: #0b192c;
        --gemini-navy: #1e3e62;
        --gemini-bright-blue: #008be6;
        --gemini-light-blue: #eef7ff;
        --gemini-gradient: linear-gradient(135deg, #0b192c 0%, #1e3e62 50%, #008be6 100%);
    }

    /* Main Container Top Margin */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero Banner Styling */
    .hero-container {
        background: var(--gemini-gradient);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(11, 25, 44, 0.25);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }

    /* Neologism Card Styling */
    .word-card {
        background-color: #ffffff;
        border: 1px solid #e0e8f5;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .word-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 139, 230, 0.12);
        border-color: #008be6;
    }
    .word-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .word-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0b192c;
    }
    .word-category {
        background-color: #eef7ff;
        color: #008be6;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .word-meaning {
        font-size: 1rem;
        color: #334155;
        margin-bottom: 0.75rem;
        line-height: 1.5;
    }
    .word-example {
        background-color: #f8fafc;
        border-left: 3px solid #008be6;
        padding: 0.5rem 0.75rem;
        font-size: 0.88rem;
        color: #475569;
        border-radius: 0 6px 6px 0;
    }

    /* Trend Badge & Metric Cards */
    .metric-box {
        background-color: #f0f7ff;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #d0e4ff;
    }
    .metric-number {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e3e62;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
    }

    /* Custom Button Style Tweaks */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Mock Database (Neologisms Data)
# ==========================================
@st.cache_data
def load_neologism_data():
    return [
        {
            "id": 1,
            "word": "추앙하다",
            "meaning": "높여 공경하고 받들다. (드라마 대사 이후 상대를 완전히 지지하고 응원한다는 의미로 대중화)",
            "category": "감정/소통",
            "origin": "드라마 '나의 해방일지'",
            "example": "너는 무슨 일을 해도 내 편이야. 난 너를 추앙해.",
            "views": 1420,
            "year": "2022~현재"
        },
        {
            "id": 2,
            "word": "중꺾마",
            "meaning": "'중요한 것은 꺾이지 않는 마음'의 줄임말. 어떤 어려움이 있어도 포기하지 않는 태도.",
            "category": "줄임말",
            "origin": "2022 LoL 월드 챔피언십 (메프트 선수 인터뷰 기사 헤드라인)",
            "example": "이번 시험 범위가 너무 많지만... 중요한 건 중꺾마야!",
            "views": 3890,
            "year": "2022~현재"
        },
        {
            "id": 3,
            "word": "알빠노",
            "meaning": "'내 알 바 아니다' (알 바 아니라는 노/No)의 합성어. 신경 쓰지 않음을 유쾌하게 표현.",
            "category": "일상/인터넷",
            "origin": "인터넷 스트리밍 커뮤니티",
            "example": "남들이 뭐라고 하든 내 길을 간다! 알빠노?",
            "views": 2510,
            "year": "2023~현재"
        },
        {
            "id": 4,
            "word": "디저트 핑계",
            "meaning": "식사를 마쳤음에도 불구하고 디저트를 먹기 위해 명분을 만들어내는 행동.",
            "category": "라이프/음식",
            "origin": "SNS 및 숏폼 콘텐츠",
            "example": "배는 부르지만 매콤한 걸 먹었으니 달달한 크로플 먹는 건 디저트 핑계지!",
            "views": 980,
            "year": "2024~현재"
        },
        {
            "id": 5,
            "word": "오운완",
            "meaning": "'오늘 운동 완료'의 줄임말. 운동 후 SNS에 인증할 때 주로 사용하는 태그.",
            "category": "줄임말",
            "origin": "인스타그램 헬스/운동 커뮤니티",
            "example": "오늘도 헬스장에서 1시간 러닝 완료! #오운완",
            "views": 4120,
            "year": "2021~현재"
        },
        {
            "id": 6,
            "word": "억까 / 억빠",
            "meaning": "억지 까기(비난) / 억지 빠기(옹호)의 줄임말. 근거 없이 비난하거나 과도하게 칭찬하는 행위.",
            "category": "인터넷/게임",
            "origin": "게임 및 인플루언서 커뮤니티",
            "example": "실수 한 번 했다고 너무 억까하는 거 아니냐?",
            "views": 3200,
            "year": "2020~현재"
        },
        {
            "id": 7,
            "word": "분위기 타다",
            "meaning": "주변 상황이나 감정의 흐름에 자연스럽게 동화되거나 흥을 돋우는 상태.",
            "category": "감정/소통",
            "origin": "대중문화 표현",
            "example": "파티 음악이 바뀌니까 다들 제대로 분위기 탔네!",
            "views": 850,
            "year": "스테디셀러"
        },
        {
            "id": 8,
            "word": "폼 미쳤다",
            "meaning": "어떤 사람의 기량, 스킬, 외모, 상태가 매우 훌륭함을 극찬하는 표현.",
            "category": "일상/인터넷",
            "origin": "유튜브 및 스포츠 커뮤니티",
            "example": "오늘 신메뉴 맛보는데 진짜 맛 폼 미쳤다!",
            "views": 5300,
            "year": "2023~현재"
        }
    ]

# Load Data
data = load_neologism_data()

# ==========================================
# 3. Sidebar Navigation & Global Filters
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/000000/book.png", width=60)
    st.title("📘 Gemini 신조어 사전")
    st.caption("요즘 트렌드 언어를 가장 쉽고 빠르게 이해하세요.")
    
    st.divider()
    
    # Navigation Menu
    menu = st.radio(
        "메뉴 이동",
        ["🏠 메인 홈 (백과사전)", "🔄 세대 간 번역기", "💡 신조어 제안하기", "📊 트렌드 통계"],
        index=0
    )
    
    st.divider()
    
    # Quick Category Filter (Global)
    st.subheader("📌 카테고리 필터")
    categories = ["전체"] + list(set([item["category"] for item in data]))
    selected_category = st.selectbox("분류 선택", categories)
    
    st.markdown("---")
    st.caption("© 2026 Neologism Dictionary App")
    st.caption("Powered by Streamlit & Gemini Style UI")


# ==========================================
# 4. Main Page Component 1: Hero Banner
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">✨ 2026 트렌드 신조어 백과사전</div>
    <div class="hero-subtitle">알쏭달쏭한 신조어부터 밈(Meme)까지, 세대 간 소통의 길잡이가 되어드립니다.</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. Tab Layout & Core Features
# ==========================================

if menu == "🏠 메인 홈 (백과사전)":
    
    # ------------------ Key Metrics Summary ------------------
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown('<div class="metric-box"><div class="metric-number">{}개</div><div class="metric-label">등록된 신조어</div></div>'.format(len(data)), unsafe_allow_html=True)
    with col_m2:
        today_word = data[0]["word"]  # Today's featured word
        st.markdown(f'<div class="metric-box"><div class="metric-number">{today_word}</div><div class="metric-label">오늘의 추천 단어</div></div>', unsafe_allow_html=True)
    with col_m3:
        top_viewed = max(data, key=lambda x: x['views'])['word']
        st.markdown(f'<div class="metric-box"><div class="metric-number">{top_viewed}</div><div class="metric-label">최다 검색 단어</div></div>', unsafe_allow_html=True)
    with col_m4:
        st.markdown('<div class="metric-box"><div class="metric-number">2026년</div><div class="metric-label">최신 데이터 업데이트</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ Search & Filter Bar ------------------
    col_search, col_sort = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 검색하고 싶은 신조어 또는 뜻을 입력하세요", "", placeholder="예: 중꺾마, 폼 미쳤다, 운동...")
    with col_sort:
        sort_option = st.selectbox("정렬 기준", ["조회순 (인기순)", "최신 등록순", "가나다순"])

    # Filter Logic
    filtered_data = data.copy()
    
    # Category Filter
    if selected_category != "전체":
        filtered_data = [d for d in filtered_data if d["category"] == selected_category]
        
    # Search Query Filter
    if search_query:
        filtered_data = [
            d for d in filtered_data 
            if search_query.lower() in d["word"].lower() or search_query.lower() in d["meaning"].lower()
        ]
        
    # Sorting Logic
    if sort_option == "조회순 (인기순)":
        filtered_data = sorted(filtered_data, key=lambda x: x["views"], reverse=True)
    elif sort_option == "최신 등록순":
        filtered_data = sorted(filtered_data, key=lambda x: x["id"], reverse=True)
    elif sort_option == "가나다순":
        filtered_data = sorted(filtered_data, key=lambda x: x["word"])

    st.markdown("---")
    
    # ------------------ Cards Display Grid ------------------
    st.subheader(f"📖 신조어 목록 ({len(filtered_data)}개)")
    
    if not filtered_data:
        st.info("💡 검색 결과가 없습니다. 다른 키워드로 검색하거나 새로운 신조어를 제안해 주세요!")
    else:
        # Displaying in 2 columns
        grid_col1, grid_col2 = st.columns(2)
        
        for idx, item in enumerate(filtered_data):
            target_col = grid_col1 if idx % 2 == 0 else grid_col2
            
            with target_col:
                # Custom Card View HTML
                card_html = f"""
                <div class="word-card">
                    <div class="word-header">
                        <span class="word-title">{item['word']}</span>
                        <span class="word-category">{item['category']}</span>
                    </div>
                    <div class="word-meaning">{item['meaning']}</div>
                    <div class="word-example">💬 <strong>예시:</strong> "{item['example']}"</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Expandable Detail Info
                with st.expander(f"🔍 '{item['word']}' 유래 & 상세정보 보기"):
                    st.write(f"**📌 유래/출처:** {item['origin']}")
                    st.write(f"**📅 유행 시기:** {item['year']}")
                    st.write(f"**👀 조회수:** {item['views']:,} 회")


elif menu == "🔄 세대 간 번역기":
    st.subheader("🔄 X/MZ 세대 - 기성세대 언어 변환기")
    st.write("일상에서 자주 쓰는 신조어를 문장으로 입력하면, 이해하기 쉬운 표준 표현으로 변환해 줍니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        user_text = st.text_area(
            "📝 신조어가 포함된 문장을 입력하세요:",
            value="오늘 운동 오운완 하고 맛집 왔는데 진짜 폼 미쳤다 중꺾마 정신으로 다 먹음!",
            height=150
        )
        translate_btn = st.button("🔵 표준어로 번역하기", use_container_width=True)
        
    with col_output:
        if translate_btn and user_text:
            # Simple keyword-based rule translator for demonstration
            translated_text = user_text
            replacements = {
                "오운완": "오늘 운동을 완료",
                "폼 미쳤다": "수준이 정말 대단하다",
                "중꺾마": "꺾이지 않는 포기하지 않는",
                "알빠노": "신경 쓰지 않는다",
                "억까": "억지로 비난하는 것",
                "추앙해": "깊이 존경하고 지지해"
            }
            
            for key, val in replacements.items():
                translated_text = translated_text.replace(key, f"**[{val}]**")
                
            st.markdown("**✨ 번역 결과 (이해하기 쉬운 표현):**")
            st.success(translated_text)
            st.info("💡 굵은 글씨로 표시된 부분은 신조어가 표준 표현으로 다듬어진 내용입니다.")
        else:
            st.markdown("**✨ 번역 결과:**")
            st.info("왼쪽에 문장을 입력하고 '표준어로 번역하기' 버튼을 눌러주세요.")


elif menu == "💡 신조어 제안하기":
    st.subheader("💡 새로운 신조어 등록 제안")
    st.write("사전에 아직 등록되지 않은 신변종 신조어가 있다면 사전 편찬팀에 제안해 주세요!")
    
    with st.form("suggestion_form"):
        new_word = st.text_input("신조어 단어", placeholder="예: 꺾이지 않는 마음")
        new_meaning = st.text_area("뜻과 의미", placeholder="단어의 정확한 뜻을 설명해 주세요.")
        new_category = st.selectbox("카테고리", ["줄임말", "감정/소통", "라이프/음식", "인터넷/게임", "기타"])
        new_example = st.text_input("사용 예시 문장", placeholder="실제 사용하는 대화예시를 입력하세요.")
        submit_btn = st.form_submit_button("제안 제출하기")
        
        if submit_btn:
            if new_word and new_meaning:
                st.balloons()
                st.success(f"🎉 '{new_word}' 제안이 접수되었습니다! 검토 후 사전에 등록될 예정입니다.")
            else:
                st.warning("⚠️ 단어와 뜻은 필수 입력 항목입니다.")


elif menu == "📊 트렌드 통계":
    st.subheader("📊 신조어 검색 및 카테고리 통계")
    st.write("현재 신조어 백과사전에 등록된 데이터 분포를 확인합니다.")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.write("##### 📌 카테고리별 신조어 비중")
        cat_counts = {}
        for item in data:
            cat = item["category"]
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        st.bar_chart(cat_counts)
        
    with col_c2:
        st.write("##### 🔥 가장 조회가 많은 인기 신조어 Top 5")
        top_5 = sorted(data, key=lambda x: x["views"], reverse=True)[:5]
        for idx, item in enumerate(top_5, 1):
            st.write(f"**{idx}. {item['word']}** ({item['category']}) - 👀 {item['views']:,}회 검색")
            st.progress(min(item['views'] / 6000, 1.0))
