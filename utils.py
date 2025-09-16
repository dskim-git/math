import streamlit as st

def set_base_page(page_title: str, page_icon: str = "📘", layout: str = "wide"):
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    _hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 2rem;}
        </style>
    """
    st.markdown(_hide_streamlit_style, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

def callout(title: str, body: str):
    st.markdown(f"#### {title}")
    st.markdown(body)
