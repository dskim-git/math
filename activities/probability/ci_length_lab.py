# activities/probability/ci_length_lab.py
import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy.stats import norm

META = {
    "title": "신뢰구간 길이 실험실",
    "description": "정규모집단(σ 알려짐)에서 모평균 100(임의), 표본크기 n, 신뢰도(1-α), 모표준편차 σ에 따라 신뢰구간 길이 L = 2·z_{α/2}·σ/√n 가 어떻게 변하는지 시각화합니다.",
    "order": 40,
}

def _z_from_conf(conf_pct: float) -> float:
    """
    conf_pct: 50~99.9 (%)
    반환: z_{alpha/2}
    """
    alpha = 1.0 - conf_pct / 100.0
    p = 1.0 - alpha / 2.0
    return float(norm.ppf(p))

def _ci_length(sig: float, n: int, conf_pct: float) -> float:
    return 2.0 * _z_from_conf(conf_pct) * (sig / math.sqrt(n))

def render():
    st.header("📏 신뢰구간 길이 실험실 (σ 알려짐)")
    st.caption("정규모집단에서 모평균의 신뢰구간 길이:  **L = 2 · z<sub>α/2</sub> · σ / √n**")

    with st.sidebar:
        st.subheader("⚙️ 설정")
        sigma = st.number_input("모표준편차 σ", min_value=0.05, max_value=50.0, value=10.0, step=0.05)
        n = st.slider("표본 크기 n", min_value=2, max_value=2000, value=30, step=1)
        conf = st.slider("신뢰도 (%)", min_value=50.0, max_value=99.9, value=95.0, step=0.1)
        st.markdown("---")
        st.markdown("**참고**: μ 값은 길이에 영향을 주지 않으므로 고정해도 무방합니다.")

    # ── 현재 설정의 길이 ──────────────────────────────────────────
    z = _z_from_conf(conf)
    L = _ci_length(sigma, n, conf)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("z\u2090\u2044\u2082", f"{z:.3f}")
    with c2:
        st.metric("신뢰구간 길이 L", f"{L:.3f}")
    with c3:
        st.metric("반길이 (L/2)", f"{L/2:.3f}")

    st.markdown("---")
    st.subheader("📈 파라미터별 길이 변화")

    # (1) n 변화에 따른 L
    n_grid = np.arange(2, 2001, 2)
    L_n = 2.0 * z * (sigma / np.sqrt(n_grid))
    fig1 = go.Figure()
    fig1.add_scatter(x=n_grid, y=L_n, mode="lines", name="L(n)", hovertemplate="n=%{x}<br>L=%{y:.3f}<extra></extra>")
    fig1.update_layout(
        title=f"n 변화에 따른 신뢰구간 길이 (σ={sigma:.2f}, 신뢰도={conf:.1f}%)",
        xaxis_title="표본 크기 n",
        yaxis_title="길이 L",
        height=360,
        margin=dict(l=40, r=20, t=50, b=40)
    )

    # (2) σ 변화에 따른 L
    sig_grid = np.linspace(0.05, 50.0, 400)
    L_sig = 2.0 * z * (sig_grid / math.sqrt(n))
    fig2 = go.Figure()
    fig2.add_scatter(x=sig_grid, y=L_sig, mode="lines", name="L(σ)", hovertemplate="σ=%{x:.2f}<br>L=%{y:.3f}<extra></extra>")
    fig2.update_layout(
        title=f"σ 변화에 따른 신뢰구간 길이 (n={n}, 신뢰도={conf:.1f}%)",
        xaxis_title="모표준편차 σ",
        yaxis_title="길이 L",
        height=360,
        margin=dict(l=40, r=20, t=50, b=40)
    )

    # (3) 신뢰도 변화에 따른 L
    conf_grid = np.linspace(50.0, 99.9, 400)
    z_grid = norm.ppf(1.0 - (1.0 - conf_grid / 100.0) / 2.0)
    L_conf = 2.0 * z_grid * (sigma / math.sqrt(n))
    fig3 = go.Figure()
    fig3.add_scatter(x=conf_grid, y=L_conf, mode="lines", name="L(conf)", hovertemplate="신뢰도=%{x:.1f}%<br>L=%{y:.3f}<extra></extra>")
    fig3.update_layout(
        title=f"신뢰도 변화에 따른 신뢰구간 길이 (n={n}, σ={sigma:.2f})",
        xaxis_title="신뢰도 (%)",
        yaxis_title="길이 L",
        height=360,
        margin=dict(l=40, r=20, t=50, b=40)
    )

    cA, cB = st.columns(2)
    with cA: st.plotly_chart(fig1, use_container_width=True)
    with cB: st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("🧮 공식 요약", expanded=False):
        st.latex(r"""
        L \;=\; 2\, z_{\alpha/2}\, \frac{\sigma}{\sqrt{n}}, \qquad
        z_{\alpha/2} = \Phi^{-1}\!\left(1-\frac{\alpha}{2}\right), \quad
        \alpha = 1-\text{conf}
        """)
        st.markdown(
            f"- 현재 설정: σ = **{sigma:.2f}**, n = **{n}**, 신뢰도 = **{conf:.1f}%**  \n"
            f"- z\u2090\u2044\u2082 = **{z:.3f}**, 길이 L = **{L:.3f}** (반길이 **{L/2:.3f}**)"
        )
