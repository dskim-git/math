import streamlit as st
from utils import set_base_page, page_header

set_base_page("확률과통계", "🎲")
page_header("확률과통계", "확률·통계 관련 시뮬레이터 모음")

st.write("왼쪽에서 하위 페이지를 펼쳐 선택하거나, 아래 바로가기 버튼을 사용하세요.")
st.page_link("pages/확률과통계/1_📊_확률_시뮬레이터.py", label="확률 시뮬레이터", icon="📊")
st.page_link("pages/확률과통계/2_🌀_정규분포_표본추출.py", label="정규분포 표본추출", icon="🌀")
st.page_link("pages/확률과통계/3_📐_원주율_몬테카를로.py", label="원주율 몬테카를로", icon="📐")
st.page_link("pages/확률과통계/4_📈_선형회귀_직선맞춤.py", label="선형회귀 직선맞춤", icon="📈")
st.page_link("pages/확률과통계/5_🚶_랜덤워크_시각화.py", label="랜덤워크 시각화", icon="🚶")
