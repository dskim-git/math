# app.py
import streamlit as st
from nav_helper import build_navigation, inject_sidebar

st.set_page_config(
    page_title="🧮 수학 시뮬레이션 허브",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_sidebar()           # 사이드바
nav = build_navigation()   # 네비 생성(모든 Page 등록)
nav.run()                  # 실행
