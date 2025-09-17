import streamlit as st
from utils import set_base_page, page_header

set_base_page("확률과통계", "🎲")
page_header("확률과통계", "확률·통계 관련 시뮬레이터 모음")

st.page_link("pages/probstat/1_binomial_sim.py", label="확률 시뮬레이터", icon="📊")
st.page_link("pages/probstat/2_normal_sampling.py", label="정규분포 표본추출", icon="🌀")
st.page_link("pages/probstat/3_pi_montecarlo.py", label="원주율 몬테카를로", icon="📐")
st.page_link("pages/probstat/4_linear_regression.py", label="선형회귀 직선맞춤", icon="📈")
st.page_link("pages/probstat/5_random_walk.py", label="랜덤워크 시각화", icon="🚶")
