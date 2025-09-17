# sections/geometry/__init__.py
import streamlit as st
from pathlib import Path

st.title("📐 기하학 메인")
st.write("기하 활동 모음입니다. 아래에서 선택해 주세요.")

folder = Path(__file__).parent
for p in sorted(x for x in folder.glob("*.py") if x.name != "__init__.py"):
    name = p.stem
    name = name[name.find("_")+1:] if "_" in name else name
    st.page_link(str(p), label=f"🔹 {name.replace('_',' ').title()}", use_container_width=True)
