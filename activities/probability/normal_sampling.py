# activities/probability/normal_sampling.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

# utils: 제목/라인(간격 최소), 앵커/점프
try:
    from utils import page_header, anchor, scroll_to
except Exception:
    # 폴백(레이아웃 최소 동작)
    def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
        if top_rule:
            st.markdown("---")
        st.markdown(f"### {icon+' ' if icon else ''}{title}")
        if subtitle:
            st.caption(subtitle)
    def anchor(name: str = "content"):
        st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name: str = "content"):
        import streamlit.components.v1 as components
        components.html(f"<script>window.location.hash='{name}'</script>", height=0)

META = {
    "title": "정규분포 표본추출",
    "description": "표본 히스토그램과 이론 밀도 비교, 표본평균/표준편차 관찰 및 구간확률 계산.",
}

# ---- 세션 키 & 기본값 (고유 키로 충돌 방지) ----
K_MU    = "norm_mu"
K_SIGMA = "norm_sigma"
K_N     = "norm_n"
K_BINS  = "norm_bins"
JUMP    = "norm_jump_flag"

DEFAULTS = {
    K_MU: 0.0,
    K_SIGMA: 1.0,
    K_N: 1000,
    K_BINS: 40,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    # 사이드바 값이 바뀌면 렌더 후 그래프 위치로 되돌아오도록 플래그
    st.session_state[JUMP] = "graph"

def render():
    _ensure_defaults()

    # ✅ 회색 라인 + 제목 세트(여백 최소, 제목은 여기서만 1회)
    page_header("정규분포 표본추출", "표본 히스토그램 vs 이론 밀도, 표본평균 관찰", icon="🌀", top_rule=True)

    # ----- 사이드바: 변경 즉시 반영(on_change) -----
    with st.sidebar:
        st.subheader("⚙️ 매개변수")

        st.number_input(
            "모평균 μ",
            value=float(st.session_state[K_MU]),
            step=0.1, format="%.3f",
            key=K_MU, on_change=_mark_changed
        )
        st.number_input(
            "모표준편차 σ (>0)",
            min_value=0.01,
            value=float(st.session_state[K_SIGMA]),
            step=0.1, format="%.3f",
            key=K_SIGMA, on_change=_mark_changed
        )
        st.slider(
            "표본 크기 n", 10, 20000,
            value=int(st.session_state[K_N]),
            key=K_N, on_change=_mark_changed
        )
        st.slider(
            "히스토그램 구간 수", 10, 100,
            value=int(st.session_state[K_BINS]),
            key=K_BINS, on_change=_mark_changed
        )

    # ----- 현재 설정 읽기 -----
    mu    = float(st.session_state[K_MU])
    sigma = float(st.session_state[K_SIGMA])
    n     = int(st.session_state[K_N])
    bins  = int(st.session_state[K_BINS])

    # 그래프 위치 앵커
    anchor("graph")

    # ----- 표본 생성 -----
    rng = np.random.default_rng()
    x = rng.normal(mu, sigma, size=n)

    # 히스토그램(밀도 정규화) 및 이론 밀도
    hist_y, hist_x = np.histogram(x, bins=bins, density=True)
    centers = 0.5 * (hist_x[:-1] + hist_x[1:])

    xs_min = min(x.min(), mu - 4 * sigma)
    xs_max = max(x.max(), mu + 4 * sigma)
    xs = np.linspace(xs_min, xs_max, 400)
    pdf = norm.pdf(xs, loc=mu, scale=sigma)

    # ----- 시각화 -----
    fig = go.Figure()
    fig.add_bar(x=centers, y=hist_y, name="표본 히스토그램(밀도)", opacity=0.7)
    fig.add_scatter(x=xs, y=pdf, name="이론 밀도", mode="lines", line=dict(width=2))
    fig.update_layout(
        title="정규분포 표본과 이론 밀도",
        xaxis_title="값",
        yaxis_title="밀도",
        legend_title="범례",
        bargap=0.05,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 표본 통계
    st.write(
        f"표본평균: **{np.mean(x):.4f}**, "
        f"표본표준편차: **{np.std(x, ddof=1):.4f}**  "
        f"(모수: μ={mu:.3f}, σ={sigma:.3f})"
    )

    # 구간확률 계산
    with st.expander("🎯 확률 계산 (P(a ≤ X ≤ b))"):
        c1, c2 = st.columns(2)
        a_val = c1.number_input("a", value=float(mu - sigma), step=0.1, format="%.3f")
        b_val = c2.number_input("b", value=float(mu + sigma), step=0.1, format="%.3f")
        if a_val <= b_val:
            prob = float(norm.cdf(b_val, mu, sigma) - norm.cdf(a_val, mu, sigma))
            st.success(f"P({a_val:.3f} ≤ X ≤ {b_val:.3f}) = **{prob:.4f}**")
        else:
            st.error("a ≤ b 를 만족하도록 값을 입력해주세요.")

    # ----- 위젯 변경 직후엔 그래프 위치로 점프 -----
    if st.session_state.get(JUMP) == "graph":
        scroll_to("graph")
        st.session_state[JUMP] = None
