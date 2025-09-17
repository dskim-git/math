# activities/probability/binomial_simulator.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(title, subtitle="", icon="", top_rule=True):
        if top_rule: st.markdown("---")
        st.markdown(f"### {icon+' ' if icon else ''}{title}")
        if subtitle: st.caption(subtitle)
    def anchor(name="content"): st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name="content"):
        import streamlit.components.v1 as components
        components.html(f"<script>window.location.hash='{name}'</script>", height=0)

META = {
    "title": "확률 시뮬레이터 (이항분포 비교)",
    "description": "베르누이/동전/주사위 실험을 반복 시뮬레이션하고 이론 이항분포와 비교합니다.",
}

# 세션 키
K_MODE, K_N, K_REPEATS, K_FACE, K_P = "prob_mode", "prob_n", "prob_repeats", "prob_face", "prob_p"
JUMP_FLAG = "prob_binom_jump"

DEFAULTS = {
    K_MODE: "동전 던지기(공정)",
    K_N: 30,
    K_REPEATS: 3000,
    K_FACE: 6,
    K_P: 0.35,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    # 위젯이 바뀌면 rerun 후 그래프 위치로 점프
    st.session_state[JUMP_FLAG] = "graph"

def render():
    _ensure_defaults()

    # 회색 줄 + 제목(여백 최소)
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교", icon="📊", top_rule=True)

    # 사이드바 (즉시 반영 + 점프 플래그)
    with st.sidebar:
        st.subheader("⚙️ 실험 설정")

        st.selectbox(
            "실험 종류", ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"],
            key=K_MODE, on_change=_mark_changed
        )
        st.slider("1회 실험 시행 수 (n)", 1, 200,
                  key=K_N, on_change=_mark_changed)
        st.slider("반복 횟수 (시뮬레이션 반복)", 100, 20000,
                  step=100, key=K_REPEATS, on_change=_mark_changed)

        if st.session_state[K_MODE] == "주사위(특정 눈)":
            st.number_input("성공 눈 (1~6)", 1, 6,
                            key=K_FACE, on_change=_mark_changed)

        if st.session_state[K_MODE] == "일반 베르누이(p)":
            st.slider("성공확률 p", 0.0, 1.0,
                      step=0.01, key=K_P, on_change=_mark_changed)

    # 현재 설정
    mode    = st.session_state[K_MODE]
    n       = int(st.session_state[K_N])
    repeats = int(st.session_state[K_REPEATS])
    face    = int(st.session_state[K_FACE])
    p_user  = float(st.session_state[K_P])

    if mode == "동전 던지기(공정)":
        p_eff, label = 0.5, "앞면(성공)"
    elif mode == "주사위(특정 눈)":
        p_eff, label = 1/6, f"{face
