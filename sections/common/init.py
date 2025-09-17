import streamlit as st
from nav_helper import activity_pages

st.title("📚 공통수학 메인")
st.write("공통수학 카테고리의 소개/사용법을 적고, 아래 활동으로 이동하세요.")

for p in activity_pages("common"):
    st.page_link(p, label=f"🔹 {p.title}", use_container_width=True)
