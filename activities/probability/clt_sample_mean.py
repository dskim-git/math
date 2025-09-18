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

    # ---- 사이드바 (위젯 '반환값'을 바로 사용) ----
    with st.sidebar:
        st.subheader("⚙️ 설정")

        dist = st.selectbox(
            "모분포", ["정규", "균등", "지수", "베르누이"],
            index=["정규", "균등", "지수", "베르누이"].index(st.session_state[K_DIST]),
            key=K_DIST, on_change=_mark_changed
        )
        n = st.slider("표본 크기 n", 1, 200,
                      value=int(st.session_state[K_N]), key=K_N, on_change=_mark_changed)
        M = st.slider("표본 개수 M (시행 수)", 200, 20000,
                      value=int(st.session_state[K_M]), step=200, key=K_M, on_change=_mark_changed)
        bins = st.slider("히스토그램 구간 수", 10, 120,
                         value=int(st.session_state[K_BINS]), key=K_BINS, on_change=_mark_changed)

        # 분포별 모수 — 모두 '슬라이더 반환값'을 변수로 저장
        mu = sigma = a = b = lmbda = p = None

        if dist == "정규":
            mu = st.slider("μ (정규)", -10.0, 10.0,
                           value=float(st.session_state[K_MU]), step=0.1,
                           key=K_MU, on_change=_mark_changed)
            sigma = st.slider("σ > 0 (정규)", 0.05, 5.0,
                              value=float(st.session_state[K_SIGMA]), step=0.05,
                              key=K_SIGMA, on_change=_mark_changed)
        elif dist == "균등":
            a = st.slider("a (하한)", -10.0, 9.9,
                          value=float(st.session_state[K_A]), step=0.1,
                          key=K_A, on_change=_mark_changed)
            b = st.slider("b (상한, a<b)", -9.9, 10.0,
                          value=float(st.session_state[K_B]), step=0.1,
                          key=K_B, on_change=_mark_changed)
            if b <= a:   # 즉시 보정(로컬 변수 + 세션 동기화)
                b = a + 0.1
                st.session_state[K_B] = b
        elif dist == "지수":
            lmbda = st.slider("λ > 0 (지수, 평균=1/λ)", 0.05, 5.0,
                              value=float(st.session_state[K_LMBDA]), step=0.05,
                              key=K_LMBDA, on_change=_mark_changed)
        else:  # 베르누이
            p = st.slider("p (베르누이 성공확률)", 0.0, 1.0,
                          value=float(st.session_state[K_P]), step=0.01,
                          key=K_P, on_change=_mark_changed)

    # ---- 그래프 위치 앵커 ----
    anchor("graph")

    # ---- 표본평균 생성: 반드시 '위젯 반환값' 변수로 계산 ----
    rng = np.random.default_rng()

    if dist == "정규":
        mu = float(mu); sigma = float(sigma)
        theo_mu, theo_sd = mu, sigma / np.sqrt(n)
        xbar = rng.normal(mu, sigma, size=(M, n)).mean(axis=1)
        desc = f"모분포: N({mu:.2f}, {sigma:.2f}²)"
        st.markdown("**모분포 PDF**")
        st.latex(rf"f_X(x)=\frac{{1}}{{{sigma:.3f}\sqrt{{2\pi}}}}\exp\!\left(-\frac{{(x-{mu:.3f})^2}}{{2\,{sigma:.3f}^2}}\right)")

    elif dist == "균등":
        a = float(a); b = float(b)
        if b <= a: b = a + 1e-6
        mu_u, var_u = (a + b) / 2.0, (b - a) ** 2 / 12.0
        theo_mu, theo_sd = mu_u, np.sqrt(var_u / n)
        xbar = rng.uniform(a, b, size=(M, n)).mean(axis=1)
        desc = f"모분포: U({a:.2f}, {b:.2f})"
        st.markdown("**모분포 PDF**")
        st.latex(rf"f_X(x)=\begin{{cases}}\dfrac{{1}}{{{b:.3f}-{a:.3f}}}, & {a:.3f}\le x\le {b:.3f} \\[4pt] 0, & \text{{else}}\end{{cases}}")

    elif dist == "지수":
        l = float(lmbda)
        mu_e, var_e = 1.0 / l, 1.0 / (l * l)
        theo_mu, theo_sd = mu_e, np.sqrt(var_e / n)
        xbar = rng.exponential(1.0 / l, size=(M, n)).mean(axis=1)
        desc = f"모분포: Exp(λ={l:.2f})"
        st.markdown("**모분포 PDF**")
        st.latex(rf"f_X(x)={l:.3f}\,e^{{-{l:.3f}x}},\quad x\ge 0")

    else:  # 베르누이
        p_ = float(p)
        mu_b, var_b = p_, p_ * (1 - p_)
        theo_mu, theo_sd = mu_b, np.sqrt(var_b / n)
        xbar = rng.binomial(n=n, p=p_, size=M) / n
        desc = f"모분포: Bernoulli(p={p_:.2f})"
        st.markdown("**모분포 PMF**")
        st.latex(rf"P(X=k)={p_:.3f}^k(1-{p_:.3f})^{{1-k}},\quad k\in\{{0,1\}}")

    # 표본평균의 정규근사 수식
    st.markdown("**표본평균의 정규근사**")
    st.latex(rf"\bar X\ \approx\ \mathcal{{N}}\!\left({theo_mu:.3f},\, {theo_sd:.3f}^2\right)")

    # ---- 시각화 ----
    fig = _draw_hist_with_normal(
        xbar, mu=theo_mu, sigma=theo_sd, bins=bins,
        title=f"표본평균 분포 vs 정규 근사 (n={n}, M={M})"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        f"{desc} → 이론값: 𝔼[ȳ]={theo_mu:.4f}, sd(ȳ)≈{theo_sd:.4f}  |  "
        f"시뮬: 평균 **{np.mean(xbar):.4f}**, 표준편차 **{np.std(xbar, ddof=1):.4f}**"
    )

    # ---- 위젯 변경 직후 그래프 위치로 복귀 ----
    if st.session_state.get(JUMP) == "graph":
        scroll_to("graph")
        st.session_state[JUMP] = None
