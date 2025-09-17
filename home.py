import streamlit as st
from utils import set_base_page, page_header

set_base_page(page_title="수학 시뮬레이션 허브", page_icon="🧮")
page_header("수학 시뮬레이션 허브", "수업에 바로 쓰는 인터랙티브 실험실")

st.write("왼쪽 **사이드바**에서 카테고리를 펼치거나, 아래 버튼으로 바로 이동하세요.")

# 카드형 카테고리 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎲 확률과통계")
    st.page_link("pages/확률과통계/0_소개_확률과통계.py", label="카테고리 소개", icon="📂")
    st.page_link("pages/확률과통계/1_📊_확률_시뮬레이터.py", label="확률 시뮬레이터", icon="📊")
    st.page_link("pages/확률과통계/2_🌀_정규분포_표본추출.py", label="정규분포 표본추출", icon="🌀")
    st.page_link("pages/확률과통계/3_📐_원주율_몬테카를로.py", label="원주율 몬테카를로", icon="📐")
    st.page_link("pages/확률과통계/4_📈_선형회귀_직선맞춤.py", label="선형회귀 직선맞춤", icon="📈")
    st.page_link("pages/확률과통계/5_🚶_랜덤워크_시각화.py", label="랜덤워크 시각화", icon="🚶")

with col2:
    st.subheader("🧩 공통수학")
    st.page_link("pages/공통수학/0_소개_공통수학.py", label="카테고리 소개", icon="📂")

    st.subheader("🧮 미적분")
    st.page_link("pages/미적분/0_소개_미적분.py", label="카테고리 소개", icon="📂")

    st.subheader("📐 기하학")
    st.page_link("pages/기하학/0_소개_기하학.py", label="카테고리 소개", icon="📂")

st.markdown("---")
st.caption("새 시뮬레이터는 원하는 카테고리 폴더에 `N_제목.py`로 추가하면 자동으로 사이드바에 정렬됩니다.")
