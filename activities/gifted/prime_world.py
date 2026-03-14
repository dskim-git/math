META = {
    "title": "기이한 소수의 세계",
    "description": "소수의 신비로운 성질과 패턴을 탐구합니다.",
    "order": 10,
    "hidden": True,
}

import streamlit as st
import streamlit.components.v1 as components


def render():
    st.title("🔢 기이한 소수의 세계")
    st.caption("소수의 신비로운 성질과 패턴을 탐구합니다.")

    st.divider()

    # ── 수업 자료를 여기에 삽입하세요 ────────────────────────────
    st.info("수업 자료를 여기에 추가하세요. (Google Slides, YouTube, PDF 등)")
