import streamlit as st

def set_base_page(page_title: str, page_icon: str = "📘", layout: str = "wide"):
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    _css = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* 제목 잘림 방지: 상단 여백 확보 */
        .block-container {padding-top: 3rem; padding-bottom: 2rem;}
        </style>
    """
    st.markdown(_css, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

# --- 간단 라우팅 유틸 (세션/쿼리파라미터 호환) ---
def goto(route: str):
    st.session_state["__ROUTE__"] = route
    try:
        st.query_params["page"] = route  # 최신
    except Exception:
        st.experimental_set_query_params(page=route)  # 구버전
    st.rerun()

def get_route(default: str = "home") -> str:
    if "__ROUTE__" in st.session_state:
        return st.session_state["__ROUTE__"]
    try:
        qp = st.query_params
        if "page" in qp and qp["page"]:
            return qp["page"]
    except Exception:
        qp = st.experimental_get_query_params()
        if "page" in qp and len(qp["page"]) > 0:
            return qp["page"][0]
    return default
