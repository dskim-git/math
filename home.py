import streamlit as st
from utils import set_base_page, page_header, goto, get_route
from sections.prob_stats.prob_simulator import render as prob_simulator
from sections.prob_stats.normal_sampling import render as normal_sampling
from sections.prob_stats.pi_montecarlo import render as pi_montecarlo
from sections.prob_stats.linear_regression import render as linear_regression
from sections.prob_stats.random_walk import render as random_walk

# 1) 공통 세팅
set_base_page(page_title="수학 시뮬레이션 허브", page_icon="🧮")

# 2) 라우트 테이블 (키 → 랜더 함수, 표시명, 카테고리)
PAGES = {
    # 확률과통계
    "prob/prob_sim":    {"title": "확률 시뮬레이터",    "group": "확률과통계", "icon": "📊", "fn": prob_simulator},
    "prob/normal":      {"title": "정규분포 표본추출",  "group": "확률과통계", "icon": "🌀", "fn": normal_sampling},
    "prob/pi":          {"title": "원주율 몬테카를로",  "group": "확률과통계", "icon": "📐", "fn": pi_montecarlo},
    "prob/linreg":      {"title": "선형회귀 직선맞춤",  "group": "확률과통계", "icon": "📈", "fn": linear_regression},
    "prob/randomwalk":  {"title": "랜덤워크 시각화",    "group": "확률과통계", "icon": "🚶", "fn": random_walk},
    # 다른 카테고리는 이후 추가
}

GROUP_ORDER = ["공통수학", "미적분", "확률과통계", "기하학"]

def sidebar_nav():
    st.sidebar.title("📚 카테고리")
    current = get_route(default="home")

    # 그룹별 아이템 구성
    groups = {g: [] for g in GROUP_ORDER}
    for key, meta in PAGES.items():
        groups[meta["group"]].append((key, f'{meta["icon"]} {meta["title"]}'))

    # Home 버튼
    if st.sidebar.button("🏠 Home으로", use_container_width=True):
        goto("home")

    # 그룹 expanders
    for g in GROUP_ORDER:
        if len(groups[g]) == 0:
            with st.sidebar.expander(f"📁 {g}", expanded=False):
                st.caption("아직 준비 중이에요.")
            continue

        # 현재 라우트가 이 그룹에 속하면 기본 펼침
        expanded = any(current == k for k, _ in groups[g])
        with st.sidebar.expander(f"📁 {g}", expanded=expanded):
            for k, label in groups[g]:
                if st.button(label, key=f"nav-{k}", use_container_width=True):
                    goto(k)

def render_home():
    page_header("수학 시뮬레이션 허브", "수업에 바로 쓰는 인터랙티브 실험실")

    st.markdown("""
    이 웹앱은 수업에 활용할 **시뮬레이션/시각화 도구**를 모아둔 허브입니다.  
    왼쪽 **카테고리**에서 원하는 항목을 펼친 뒤 하위 페이지를 선택하세요.  
    아래 **바로가기 버튼**으로도 자주 쓰는 페이지에 빠르게 들어갈 수 있어요. 😄
    """)

    st.subheader("🔖 확률과통계 바로가기")
    cols = st.columns(3)
    shortcuts = [
        ("📊 확률 시뮬레이터", "prob/prob_sim"),
        ("🌀 정규분포 표본추출", "prob/normal"),
        ("📐 원주율 몬테카를로", "prob/pi"),
        ("📈 선형회귀 직선맞춤", "prob/linreg"),
        ("🚶 랜덤워크 시각화", "prob/randomwalk"),
    ]
    for i, (label, route) in enumerate(shortcuts):
        if cols[i % 3].button(label, use_container_width=True, key=f"home-shortcut-{route}"):
            goto(route)

    with st.expander("📂 내 자료(CSV) 빠르게 불러오기/미리보기"):
        up = st.file_uploader("CSV 업로드", type=["csv"])
        if up is not None:
            import pandas as pd
            df = pd.read_csv(up)
            st.dataframe(df.head(50))
            st.session_state["__LAST_UPLOADED_DF__"] = df
            st.success("세션에 저장했어요. 다른 페이지에서도 사용 가능!")

# --- 앱 실행 흐름 ---
sidebar_nav()
route = get_route(default="home")

if route == "home":
    render_home()
elif route in PAGES:
    meta = PAGES[route]
    page_header(f'{meta["icon"]} {meta["title"]}', f'{meta["group"]} / {meta["title"]}')
    meta["fn"]()  # 해당 페이지 렌더 함수 호출
else:
    st.error("존재하지 않는 페이지 경로입니다. Home으로 이동합니다.")
    goto("home")
