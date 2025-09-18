# activities/probability/clt_sample_mean.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

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
    "title": "CLT: 표본평균의 분포",
    "description": "모분포가 달라도 n이 커지면 표본평균 분포가 정규에 가까워지는 현상을 시각화합니다.",
}

# --- 세션 키 & 기본값 ---
K_DIST   = "clt_dist"
K_N      = "clt_n"
K_M      = "clt_m"
K_BINS   = "clt_bins"
# 분포별 모수
K_MU     = "clt_norm_mu"
K_SIGMA  = "clt_norm_sigma"
K_A      = "clt_unif_a"
K_B      = "clt_unif_b"
K_LMBDA  = "clt_exp_lambda"
K_P      = "clt_bern_p"
JUMP     = "clt_jump"

DEFAULTS = {
    K_DIST:  "정규",
    K_N:     30,
    K_M:     8000,
    K_BINS:  40,
    K_MU:    0.0,
    K_SIGMA: 1.0,
    K_A:    -1.0,
    K_B:     1.0,
    K_LMBDA: 1.0,
    K_P:     0.3,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    st.session_state[JUMP] = "graph"

def _draw_hist_with_normal(x, mu, sigma, bins, title):
    hist_y, hist_x = np.histogram(x, bins=bins, density=True)
    centers = 0.5 * (hist_x[:-1] + hist_x[1:])
    xs = np.linspace(min(centers.min(), mu - 4*sigma), max(centers.max(), mu + 4*sigma), 400)
    pdf = norm.pdf(xs, loc=mu, scale=sigma)
    fig = go.Figure()
    fig.add_bar(x=centers, y=hist_y, name="시뮬 히스토그램(밀도)", opacity=0.7)
    fig.add_scatter(x=xs, y=pdf, mode="lines", name="정규 근사(이론)", line=dict(width=2))
    fig.update_layout(title=title, xaxis_title="값", yaxis_title="밀도", legend_title="범례", bargap=0.05)
    return fig

def render():
    _ensure_defaults()
    page_header("중심극한정리 (CLT) 데모", "표본평균의 분포가 정규로 수렴하는 모습을 관찰합니다.", icon="📈", top_rule=True)

    # ---- 사이드바: 즉시 반영되는 슬라이더 기반 컨트롤 ----
    with st.sidebar:
        st.subheader("⚙️ 설정")

        dist = st.selectbox(
            "모분포", ["정규", "균등", "지수", "베르누이"],
            index=["정규", "균등", "지수", "베르누이"].index(st.session_state[K_DIST]),
            key=K_DIST, on_change=_mark_changed
        )
        n = st.slider("표본 크기 n", 1, 200, value=int(st.session_state[K_N]),
                      key=K_N, on_change=_mark_changed)
        M = st.slider("표본 개수 M (시행 수)", 200, 20000, value=int(st.session_state[K_M]),
                      step=200, key=K_M, on_change=_mark_changed)
        bins = st.slider("히스토그램 구간 수", 10, 120, value=int(st.session_state[K_BINS]),
                         key=K_BINS, on_change=_mark_changed)

        # 분포별 모수
