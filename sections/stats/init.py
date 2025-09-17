# sections/stats/__init__.py
import streamlit as st
from pathlib import Path

st.title("🎲 확률과통계 메인")
st.write("확률·통계 활동 목록입니다. 새로운 파일을 이 폴더에 추가하면 자동으로 나타납니다.")

folder = Path(__file__).parent
for p in sorted(x for x in folder.glob("*.py") if x.name != "__init__.py"):
    base = p.stem
    base = base[base.find("_")+1:] if "_" in base else base
    st.page_link(str(p), label=f"🔹 {base.replace('_',' ').title()}", use_container_width=True)
