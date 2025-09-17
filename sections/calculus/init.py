import streamlit as st
from nav_helper import activity_pages

st.title("∫ 미적분학 메인")
st.write("미적분 활동 목록입니다.")

for p in activity_pages("calculus"):
    st.page_link(p, label=f"🔹 {p.title}", use_container_width=True)
