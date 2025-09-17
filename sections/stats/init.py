import streamlit as st
from nav_helper import activity_pages

st.title("🎲 확률과통계 메인")
st.write("확률·통계 활동 목록입니다.")

for p in activity_pages("stats"):
    st.page_link(p, label=f"🔹 {p.title}", use_container_width=True)
