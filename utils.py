import streamlit as st
import streamlit.components.v1 as components

def page_header(title: str, subtitle: str = "", icon: str = ""):
    """페이지 상단 제목/부제. render에서만 호출해 '제목 1회 출력' 원칙 유지."""
    if icon:
        st.markdown(f"### {icon} {title}")
    else:
        st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

def anchor(name: str = "content"):
    """현재 위치에 스크롤 앵커를 심습니다."""
    st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)

def scroll_to(name: str = "content"):
    """앵커 이름으로 즉시 스크롤."""
    components.html(f"<script>window.location.hash = '{name}'</script>", height=0)
