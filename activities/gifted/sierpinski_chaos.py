META = {
    "title": "시어핀스키 삼각형과 카오스 게임",
    "description": "프랙털의 아름다움과 카오스 게임의 원리를 탐구합니다.",
    "order": 20,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components


def render():
    st.title("🔺 시어핀스키 삼각형과 카오스 게임")
    st.caption("프랙털의 아름다움과 카오스 게임의 원리를 탐구합니다.")

    st.divider()

    # ── 수업 자료를 여기에 삽입하세요 ────────────────────────────
    st.info("수업 자료를 여기에 추가하세요. (Google Slides, YouTube, PDF 등)")
