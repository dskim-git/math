import streamlit as st

def set_base_page(page_title: str, page_icon: str = "📘", layout: str = "wide"):
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    _style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* 상단 제목 잘림 방지 */
        .block-container {padding-top: 3rem; padding-bottom: 2rem;}
        </style>
    """
    st.markdown(_style, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")
