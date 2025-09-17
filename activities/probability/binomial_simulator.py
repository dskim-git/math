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

# 상태 키(다른 액티비티와 충돌 방지)
SCROLL_FLAG = "prob_binom_scroll_to"

# 위젯 키 (세션 상태에 저장될 이름)
K_MODE     = "prob_mode"
K_N        = "prob_n"
K_REPEATS  = "prob_repeats"
K_FACE     = "prob_face"
K_P        = "prob_p"

DEFAULTS = {
    K_MODE:    "동전 던지기(공정)",
    K_N:       30,
    K_REPEATS: 3000,
    K_FACE:    6,
    K_P:       0.35,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    # 어떤 위젯이든 변경되면 그래프 위치로 복귀 플래그 설정
    st.session_state[SCROLL_FLAG] = "graph"

def render():
    _ensure_defaults()

    # ✅ 제목은 render에서만 1회 출력
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교", icon="📊")

    # ----- 사이드바 (즉시 반영: on_change 콜백 사용, 폼 사용 안 함) -----
    with st.sidebar:
        st.subheader("⚙️ 실험 설정")

        st.selectbox(
            "실험 종류",
            ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"],
            key=K_MODE,
            on_change=_mark_changed
        )

        st.slider(
            "1회 실험 시행 수 (n)", 1, 200,
            key=K_N,
            on_change=_mark_changed
        )

        st.slider(
            "반복 횟수 (시뮬레이션 반복)", 100, 20000,
            step=100,
            key=K_REPEATS,
            on_change=_mark_changed
        )

        if st.session_state[K_MODE] == "주사위(특정 눈)":
            st.number_input(
                "성공 눈 (1~6)", min_value=1, max_value=6,
                key=K_FACE,
                on_change=_mark_changed
            )

        if st.session_state[K_MODE] == "일반 베르누이(p)":
            st.slider(
                "성공확률 p", 0.0, 1.0,
                step=0.01,
                key=K_P,
                on_change=_mark_changed
            )

    # ----- 현재 설정 읽기 -----
    mode    = st.session_state[K_MODE]
    n       = int(st.session_state[K_N])
    repeats = int(st.session_state[K_REPEATS])
    face    = int(st.session_state[K_FACE])
    p       = float(st.session_state[K_P])

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

    # ----- 위젯 변경 직후엔 그래프 위치로 복귀 -----
    if st.session_state.get(SCROLL_FLAG) == "graph":
        scroll_to("graph")
        st.session_state[SCROLL_FLAG] = None
