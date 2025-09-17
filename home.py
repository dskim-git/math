# home.py
import streamlit as st
from nav_helper import CATEGORY_INFO, category_main_page, inject_sidebar

st.title("🧮 수학 시뮬레이션 허브")
st.markdown(
    """
**수학 수업에서 바로 쓰는 시뮬레이션 모음집**  
- 상단/사이드바에서 과목을 선택해 활동으로 이동하세요.  
- 새 활동은 해당 과목 폴더에 `.py` 파일 추가만 하면 자동 반영됩니다.
"""
)

cols = st.columns(4)
for (key, label, icon), col in zip(CATEGORY_INFO, cols):
    with col:
        st.page_link(
            category_main_page(key),      # ✅ Page 객체를 직접 전달
            label=f"{icon} {label}",
            help=f"{label} 메인으로 이동",
            use_container_width=True,
        )

inject_sidebar()
