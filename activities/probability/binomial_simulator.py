import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# --- utils가 있으면 사용, 없으면 안전한 대체 함수 사용 ---
try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(title: str, subtitle: str = "", icon: str = "📊"):
        st.markdown(f"### {icon} {title}")
        if subtitle:
            st.caption(subtitle)
    def anchor(name: str = "content"):
        st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name: str = "content"):
        components.html(f"<script>window.location.hash = '{name}'</script>", height=0)

META = {
    "title": "확률 시뮬레이터 (이항분포 비교)",
    "description": "베르누이/동전/주사위 실험을 반복 시뮬레이션하고 이론 이항분포와 비교합니다.",
}

# 이 액티비티만의 상태 키(다른 액티비티와 충돌 방지)
STATE_KEY = "prob_binom_cfg"
SCROLL_FLAG = "prob_binom_scroll_to"

DEFAULTS = {
    "mode": "동전 던지기(공정)",
    "n": 30,
    "repeats": 3000,
    "face": 6,
    "p": 0.35,
}

def _ensure_state():
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = DEFAULTS.copy()

def render():
    _ensure_state()
    cfg = st.session_state[STATE_KEY]

    # ✅ 제목은 여기에서만 1번 출력
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교", icon="📊")

    # ----- 사이드바: 폼(조작 중 rerun 없음) -----
    with st.sidebar.form("binom_form", clear_on_submit=False):
        st.subheader("⚙️ 실험 설정")

        mode = st.selectbox(
            "실험 종류",
            ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"],
            index=["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"].index(cfg["mode"]),
            key="prob_mode_input"
        )

        n = st.slider("1회 실험 시행 수 (n)", 1, 200, cfg["n"], key="prob_n_input")
        repeats = st.slider("반복 횟수 (시뮬레이션 반복)", 100, 20000, cfg["repeats"], step=100, key="prob_repeats_input")

        face = cfg["face"]
        if mode == "주사위(특정 눈)":
            face = st.number_input("성공 눈 (1~6)", min_value=1, max_value=6, value=cfg["face"], step=1, key="prob_face_input")

        p = cfg["p"]
        if mode == "일반 베르누이(p)":
            p = st.slider("성공확률 p", 0.0, 1.0, cfg["p"], 0.01, key="prob_p_input")

        submitted = st.form_submit_button("적용하기", use_container_width=True)

    # ----- 제출 시에만 상태 업데이트 → 이후 계산은 상태값으로 -----
    if submitted:
        new_cfg = {
            "mode": st.session_state.get("prob_mode_input", cfg["mode"]),
            "n": st.session_state.get("prob_n_input", cfg["n"]),
            "repeats": st.session_state.get("prob_repeats_input", cfg["repeats"]),
            "face": st.session_state.get("prob_face_input", cfg["face"]) if mode == "주사위(특정 눈)" else cfg["face"],
            "p": st.session_state.get("prob_p_input", cfg["p"]) if mode == "일반 베르누이(p)" else cfg["p"],
        }
        st.session_state[STATE_KEY] = new_cfg
        st.session_state[SCROLL_FLAG] = "graph"
        st.rerun()

    # ----- 여기부터는 '확정된 상태값'으로 계산 -----
    cfg = st.session_state[STATE_KEY]  # 최신 상태 재읽기
    mode = cfg["mode"]
    n = int(cfg["n"])
    repeats = int(cfg["repeats"])
    face = int(cfg["face"])
    p = float(cfg["p"])

    # 모드별 p/라벨
    if mode == "동전 던지기(공정)":
        p_eff = 0.5
        label = "앞면(성공)"
    elif mode == "주사위(특정 눈)":
        p_eff = 1/6
        label = f"{face} 눈"
    else:  # 일반 베르누이(p)
        p_eff = p
        label = "성공"

    st.write(f"**성공 조건:** {label} | **성공확률 p:** {p_eff:.3f}")

    # ----- 그래프 위치 앵커 -----
    anchor("graph")

    # ----- 시뮬레이션 -----
    rng = np.random.default_rng()
    sim = rng.binomial(n=n, p=p_eff, size=repeats)

    counts = np.bincount(sim, minlength=n+1)
    k_emp = np.nonzero(counts)[0]
    emp_prob = counts[counts > 0] / repeats

    k = np.arange(0, n+1)
    theo = binom.pmf(k, n, p_eff)

    fig = go.Figure()
    fig.add_bar(x=k_emp, y=emp_prob, name="시뮬레이션", opacity=0.7)
    fig.add_scatter(x=k, y=theo, mode="lines+markers", name="이론(이항분포)", line=dict(width=2))
    fig.update_layout(
        title=f"이항분포 비교 (n={n}, p={p_eff:.3f})",
        xaxis_title="성공 횟수",
        yaxis_title="확률",
        legend_title="범례",
        bargap=0.05,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**포인트**: 시행 수가 커질수록 시뮬레이션 막대와 이론 곡선이 점점 가까워집니다 (대수의 법칙).")

    with st.expander("📎 시뮬레이션 원자료 보기"):
        st.dataframe({"성공횟수": sim[: min(1000, repeats)]})

    # ----- 제출 후 그래프 위치로 복귀 -----
    if st.session_state.get(SCROLL_FLAG) == "graph":
        scroll_to("graph")
        st.session_state[SCROLL_FLAG] = None
