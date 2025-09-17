import streamlit as st
from nav_helper import activity_pages

st.title("📐 기하학 메인")
st.write("기하 활동 목록입니다.")

for p in activity_pages("geometry"):
    st.page_link(p, label=f"🔹 {p.title}", use_container_width=True)
