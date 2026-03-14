META = {
    "title": "작도 게임",
    "description": "컴퍼스와 눈금 없는 자만으로 도형을 작도하는 원리를 탐구합니다.",
    "order": 40,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components


def render():
    st.title("📐 작도 게임")
    st.caption("컴퍼스와 눈금 없는 자만으로 도형을 작도하는 원리를 탐구합니다.")

    st.divider()

    # ── 수업 자료를 여기에 삽입하세요 ────────────────────────────
    st.info("수업 자료를 여기에 추가하세요. (Google Slides, YouTube, PDF 등)")
