# -*- coding: utf-8 -*-
import streamlit as st
from nav_helper import build_navigation, inject_sidebar

st.set_page_config(
    page_title="🧮 수학 시뮬레이션 허브",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_sidebar()
nav = build_navigation()
nav.run()
