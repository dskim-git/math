import streamlit as st
from pathlib import Path
from utils import set_base_page, page_header

# 앱 기본 설정
set_base_page(page_title="수학 시뮬레이션 허브", page_icon="🧮")
page_header("수학 시뮬레이션 허브", "수업에 바로 쓰는 인터랙티브 실험실")

st.write("왼쪽 **사이드바**에서 카테고리를 펼치거나, 아래 버튼으로 바로 이동하세요.")

# 안전 링크: 경로가 없으면 앱이 죽지 않도록 처리
BASE = Path(__file__).parent  # /mount/src/math
def safe_page_link(rel_path: str, label: str, icon: str):
    target = BASE / rel_path
    if target.exists():
        st.page_link(rel_path, label=label, icon=icon)
    else:
        st.warning(f"⚠️ 페이지가 없습니다: {rel_path}")

# 카테고리 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎲 확률과통계")
    safe_page_link("pages/probstat/0_index.py", "카테고리 소개", "📂")
    safe_page_link("pages/probstat/1_binomial_sim.py", "확률 시뮬레이터", "📊")
    safe_page_link("pages/probstat/2_normal_sampling.py", "정규분포 표본추출", "🌀")
    safe_page_link("pages/probstat/3_pi_montecarlo.py", "원주율 몬테카를로", "📐")
    safe_page_link("pages/probstat/4_linear_regression.py", "선형회귀 직선맞춤", "📈")
    safe_page_link("pages/probstat/5_random_walk.py", "랜덤워크 시각화", "🚶")

with col2:
    st.subheader("🧩 공통수학")
    safe_page_link("pages/common/0_index.py", "카테고리 소개", "📂")

    st.subheader("🧮 미적분")
    safe_page_link("pages/calculus/0_index.py", "카테고리 소개", "📂")

    st.subheader("📐 기하학")
    safe_page_link("pages/geometry/0_index.py", "카테고리 소개", "📂")

st.markdown("---")
st.caption("새 시뮬레이터는 원하는 카테고리 폴더에 `N_slug.py`로 추가하면 자동으로 사이드바에 정렬됩니다.")
