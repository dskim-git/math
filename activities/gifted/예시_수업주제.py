"""
영재 수업 주제 파일 예시.
이 파일을 복사해서 새로운 수업 주제를 추가하세요.
파일명은 수업 주제를 나타내는 이름으로 지정하면 됩니다 (예: 정다면체_탐구.py, 황금비.py 등).
"""

META = {
    "title": "예시 수업 주제",
    "description": "이 파일을 복사하여 새로운 수업 주제 페이지를 만들어 보세요.",
    "order": 100,
    "hidden": True,   # 실제 수업 주제 파일은 False로 변경
}

import streamlit as st
import streamlit.components.v1 as components


def render():
    st.title("📐 예시 수업 주제")
    st.caption("아래 내용을 실제 수업 자료로 교체하세요.")

    # ── 수업 자료 삽입 예시 ──────────────────────────────────────────
    # Google Slides 삽입 예시:
    # components.iframe(
    #     "https://docs.google.com/presentation/d/[ID]/embed?start=false&loop=false&delayms=3000",
    #     height=500,
    # )

    # YouTube 삽입 예시:
    # st.video("https://www.youtube.com/watch?v=VIDEO_ID")

    # 텍스트 설명:
    st.info("이 파일을 복사한 뒤 META의 title/description을 수정하고, render() 안에 수업 자료를 삽입하세요.")

    st.markdown("""
    ### 수업 자료 삽입 방법
    - **Google Slides**: `components.iframe(embed_url, height=500)`
    - **YouTube**: `st.video("watch URL")`
    - **Google Sheet**: `components.iframe(embed_url, height=400)`
    - **PDF**: `embed_pdf(url)` *(home.py의 embed_pdf 함수 import 후 사용)*
    """)
