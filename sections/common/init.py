# sections/common/__init__.py
import streamlit as st
from pathlib import Path

st.title("📚 공통수학 메인")
st.markdown(
    """
이 영역에는 **공통수학** 카테고리의 소개, 수업 포인트, 사용법 등을 적을 수 있어요.  
아래 목록에서 활동을 선택해 바로 이동하세요.
"""
)

# 현재 폴더의 활동 파일 자동 나열
folder = Path(__file__).parent
files = sorted(p for p in folder.glob("*.py") if p.name != "__init__.py")

for p in files:
    title = p.stem
    title = title[title.find("_")+1:] if "_" in title else title
    title = title.replace("_", " ").title()
    st.page_link(str(p), label=f"🔹 {title}", use_container_width=True)
