import streamlit as st

def set_base_page(title: str, icon: str = "📊"):
    # home.py에서 set_page_config를 이미 했으므로 여기선 배지 느낌만
    st.markdown(f"### {icon} {title}")

def page_header(title: str, subtitle: str = ""):
    st.header(title)
    if subtitle:
        st.caption(subtitle)
