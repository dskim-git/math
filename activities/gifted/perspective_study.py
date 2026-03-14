META = {
    "title": "사진과 그림을 활용한 시선에 대한 연구",
    "description": "사진과 그림 속 시선의 방향과 수학적 구조를 분석합니다.",
    "order": 30,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components


def render():
    st.title("👁 사진과 그림을 활용한 시선에 대한 연구")
    st.caption("사진과 그림 속 시선의 방향과 수학적 구조를 분석합니다.")

    st.divider()

    # ── 수업 자료를 여기에 삽입하세요 ────────────────────────────
    st.info("수업 자료를 여기에 추가하세요. (Google Slides, YouTube, PDF 등)")
