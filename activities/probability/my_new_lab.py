import streamlit as st
META = {
    "title": "새 실험",
    "description": "요약 설명",
    # "order": 120,      # 선택: 사이드바/과목 메인 정렬에 힌트
    # "hidden": False,   # mini/에서도 보이게 하려면 False
}
def render():
    st.write("Hello, Mathlab!")
