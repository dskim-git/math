# app.py
import streamlit as st
from nav_helper import build_navigation, inject_sidebar

st.set_page_config(
    page_title="🧮 수학 시뮬레이션 허브",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 공통 사이드바(접이식: 상위 클릭 시 하위 노출)
inject_sidebar()

# 상단 내비게이션(홈/과목/활동 자동 탐색)
nav = build_navigation()
nav.run()
