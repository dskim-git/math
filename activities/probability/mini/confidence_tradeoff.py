import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from math import sqrt
from typing import Tuple

PAGE_META = {
    "title": "신뢰도 vs 정확도(신뢰구간 길이)",
    "group": "확률과통계",
    "icon": "🎯",
}

# -----------------------------
# 유틸: z-분위수 (정확/근사)
# -----------------------------
from math import erf, erfc, sqrt, log

def norm_ppf(p: float) -> float:
    """표준정규 분위수 근사 (p∈(0,1)) — Wichura/AS241의 간단화 근사"""
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0,1)")
    # 중앙·꼬리 분할 근사 (Peter John Acklam 근사)
    a = [ -3.969683028665376e+01,  2.209460984245205e+02,
          -2.759285104469687e+02,  1.383577518672690e+02,
          -3.066479806614716e+01,  2.506628277459239e+00 ]
    b = [ -5.447609879822406e+01,  1.615858368580409e+02,
          -1.556989798598866e+02,  6.680131188771972e+01,
          -1.328068155288572e+01 ]
    c = [ -7.784894002430293e-03, -3.223964580411365e-01,
          -2.400758277161838e+00, -2.549732539343734e+00,
           4.374664141464968e+00,  2.938163982698783e+00 ]
    d = [  7.784695709041462e-03,  3.224671290700398e-01,
           2.445134137142996e+00,  3.754408661907416e+00 ]
    plow  = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = np.sqrt(-2*np.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
               ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    if p > phigh:
        q = np.sqrt(-2*np.log(1-p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                 ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    q = p - 0.5
    r = q*q
    return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / \
           (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)

def z(alpha: float) -> float:
    """상단 꼬리 확률 alpha에 대한 z_{1-alpha} (즉 P(Z>z)=alpha)"""
    return norm_ppf(1.0 - alpha)

# -----------------------------
# 1) 같은 신뢰도에서 '가장 짧은' 신뢰구간 확인
# -----------------------------
def ci_length_asym(alpha: float, share_left: float, se: float) -> Tuple[float,float,float]:
    """
    alpha=1-신뢰도, share_left∈[0,1] (왼쪽 꼬리 비율).
    CI for μ with known σ: [x̄ + z_{alpha_L}·se, x̄ + z_{1-alpha_R}·se]
    길이 = ( z_{1-alpha_R} - z_{alpha_L} ) * se
    """
    aL = alpha * share_left
    aR = alpha - aL
    zl = norm_ppf(aL)         # z_{aL} : 음수(보통)
    zr = norm_ppf(1 - aR)     # z_{1-aR} : 양수(보통)
    L = (zr - zl) * se
    return L, zl, zr

def draw_pdf_with_shade(zl: float, zr: float):
    xs = np.linspace(-4, 4, 600)
    pdf = 1/np.sqrt(2*np.pi)*np.exp(-xs**2/2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=pdf, mode="lines", name="N(0,1) 밀도"))
    # 음영 채우기
    mask = (xs>=zl) & (xs<=zr)
    fig.add_trace(go.Scatter(x=xs[mask], y=pdf[mask], fill='tozeroy', mode='lines',
                             name="신뢰구간에 해당하는 면적(고정된 신뢰도)"))
    fig.add_vline(x=zl, line_dash="dot", line_color="gray")
    fig.add_vline(x=zr, line_dash="dot", line_color="gray")
    fig.update_layout(height=340, xaxis_title="표준화된 스케일 (Z)", yaxis_title="밀도",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.02))
    return fig

# -----------------------------
# 2) 신뢰도(1-α)에 따른 '효율' 곡선
#    - 대칭 CI 전제: 길이 L(α)=2·z_{1-α/2}·se
#    - 효율1: (신뢰도)/(길이)  (단순 비율)
#    - 효율2: U(α)= (신뢰도) − λ·(길이)  (교사/상황에 맞춰 가중 조정)
# -----------------------------
def length_symmetric(alpha: float, se: float) -> float:
    return 2.0 * z(alpha/2.0) * se

def make_efficiency_curves(se: float, lam: float):
    CLs = np.linspace(0.50, 0.999, 400)  # 50%~99.9%
    alphas = 1 - CLs
    Ls = np.array([length_symmetric(a, se) for a in alphas])
    ratio = CLs / Ls
    util  = CLs - lam * Ls
    return CLs, Ls, ratio, util

# -----------------------------
# 메인 렌더
# -----------------------------
def render():
    st.sidebar.subheader("⚙️ 표본 정보")
    sigma = st.sidebar.number_input("모표준편차 σ (알고 있다고 가정)", value=10.0, step=0.5)
    n     = st.sidebar.number_input("표본 크기 n", min_value=1, value=25, step=1)
    se = float(sigma / np.sqrt(n))

    st.markdown("### 1) 같은 신뢰도에서 **가장 짧은 신뢰구간**은 왜 대칭일까?")
    colA, colB = st.columns([2,1])
    with colB:
        CL = st.slider("신뢰도 (1−α)", min_value=0.50, max_value=0.999, value=0.95, step=0.001, format="%.3f")
        alpha = 1.0 - CL
        share_left = st.slider("왼쪽 꼬리 비율 (α_L/α)", 0.0, 1.0, 0.50, step=0.01)

    # 현재 비대칭 구간의 길이
    L, zl, zr = ci_length_asym(alpha, share_left, se)
    # 대칭(최적) 구간
    L_sym = length_symmetric(alpha, se)
    zl_sym, zr_sym = -z(alpha/2.0), z(alpha/2.0)

    with colA:
        st.caption("표준정규에서 면적을 고정(=신뢰도 유지)한 채로 경계를 움직입니다.")
        fig = draw_pdf_with_shade(zl, zr)
        # 최적(대칭) 경계도 가이드로 표시
        fig.add_vline(x=zl_sym, line=dict(color="purple", width=2), annotation_text="대칭 경계")
        fig.add_vline(x=zr_sym, line=dict(color="purple", width=2))
        st.plotly_chart(fig, use_container_width=True)

    # 길이 수치 비교
    c1, c2, c3 = st.columns(3)
    c1.metric("현재 구간 길이", f"{L:.4f}")
    c2.metric("대칭 구간 길이(최소)", f"{L_sym:.4f}")
    c3.metric("길이 차이(현재−대칭)", f"{(L - L_sym):.4f}")

    # 비대칭 정도에 따른 길이 그래프
    r_grid = np.linspace(0, 1, 201)
    lengths = [ci_length_asym(alpha, r, se)[0] for r in r_grid]
    fig_len = go.Figure()
    fig_len.add_trace(go.Scatter(x=r_grid, y=lengths, mode="lines", name="길이 L(α_L/α)"))
    fig_len.add_vline(x=0.5, line_color="purple", line_dash="dash",
                      annotation_text="대칭(최소)", annotation_position="top")
    fig_len.add_vline(x=share_left, line_color="gray", line_dash="dot",
                      annotation_text="현재 비율")
    fig_len.update_layout(height=320, xaxis_title="왼쪽 꼬리 비율  α_L / α",
                          yaxis_title=f"구간 길이  (단위: {se:.4f}×z 차이)")
    st.plotly_chart(fig_len, use_container_width=True)

    st.markdown(
        """
        **설명**: 신뢰도(면적) \\(1-\\alpha\\) 를 고정하면, 가능한 신뢰구간은 많지만  
        길이 \\(L = (z_{1-\\alpha_R}-z_{\\alpha_L})\\,\\text{SE}\\) 가 **최소**가 되려면  
        \\(\\alpha_L = \\alpha_R = \\alpha/2\\) (즉, 표본평균을 중심으로 **좌우대칭**)이어야 합니다.
        """
    )

    st.divider()

    st.markdown("### 2) 왜 95%를 많이 쓸까? — 여러 ‘효율’ 기준으로 비교해 보기")
    st.caption("대칭 신뢰구간(최소 길이)만 비교합니다. 표본오차 SE=σ/√n 이 클수록 길이는 전체적으로 길어집니다.")
    col1, col2 = st.columns([1.2, 1])
    with col2:
        metric = st.selectbox("효율 기준 선택", ["비율: (신뢰도)/(길이)", "효용: (신뢰도) − λ·(길이)"])
        lam = 0.12
        if metric.startswith("효용"):
            lam = st.slider("λ (길이에 대한 패널티 가중치)", 0.00, 0.50, 0.12, 0.01)

    CLs, Ls, ratio, util = make_efficiency_curves(se, lam)

    with col1:
        if metric.startswith("비율"):
            y = ratio
            ylab = "효율 = (신뢰도) / (길이)"
        else:
            y = util
            ylab = "효용 = (신뢰도) − λ·(길이)"

        fig_eff = go.Figure()
        fig_eff.add_trace(go.Scatter(x=CLs, y=y, mode="lines", name=ylab))
        # 95% 표시
        cl95 = 0.95
        a95 = 1 - cl95
        L95 = length_symmetric(a95, se)
        y95 = (cl95 / L95) if metric.startswith("비율") else (cl95 - lam * L95)
        fig_eff.add_vline(x=0.95, line_dash="dash", line_color="gray",
                          annotation_text="95%", annotation_position="top")
        # 최대점(수치)
        idx_max = int(np.argmax(y))
        cl_star = float(CLs[idx_max])
        y_star  = float(y[idx_max])
        fig_eff.add_vline(x=cl_star, line_color="purple",
                          annotation_text=f"최대≈{cl_star:.3f}", annotation_position="bottom")
        fig_eff.update_layout(height=340, xaxis_title="신뢰도 (1−α)",
                              yaxis_title=ylab)
        st.plotly_chart(fig_eff, use_container_width=True)

    # 수치 요약
    c1, c2, c3 = st.columns(3)
    c1.metric("SE = σ/√n", f"{se:.4f}")
    c2.metric("95% 대칭 구간 길이", f"{L95:.4f}")
    c3.metric("현재 기준에서 최대 효율 신뢰도", f"{cl_star:.3f}")

    st.markdown(
        """
        **해석 가이드**  
        - 단순 **비율** 기준 \\((1-\\alpha)/L\\) 은 **신뢰도가 낮을수록** 커지므로, 이 기준만으로는 95%를
          ‘최적’이라 말하기 어렵습니다.  
        - 수업/연구에서는 대개 **정확도(짧은 길이)** 와 **신뢰도(높은 면적)** 를 **동시에** 고려해야 하므로  
          \\( U(\\alpha)= (1-\\alpha) - \\lambda L(\\alpha) \\)와 같은 **가중 효용**을 생각해 볼 수 있어요.  
          적절한 \\(\\lambda\\) 를 두면 **약 95%** 근처에서 균형점이 나타나는 걸 시각적으로 확인할 수 있습니다.  
        - 즉, 95%는 “관례”이면서도 **신뢰도와 정확도의 균형**이라는 교육적 설명을 곁들일 수 있습니다.
        """
    )
