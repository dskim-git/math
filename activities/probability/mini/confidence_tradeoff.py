import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Tuple

PAGE_META = {
    "title": "신뢰도 vs 정확도(신뢰구간 길이)",
    "group": "확률과통계",
    "icon": "🎯",
}

# -----------------------------
# 표준정규 분위수 근사 (Acklam)
# -----------------------------
def norm_ppf(p: float) -> float:
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow = 0.02425
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
    """상단 꼬리확률 alpha에 대한 z_{1-alpha}"""
    return norm_ppf(1.0 - alpha)

# -----------------------------
# 1) 같은 신뢰도에서 비대칭 구간 길이(파트1 그대로)
# -----------------------------
def ci_length_asym(alpha: float, share_left: float, se: float) -> Tuple[float, float, float]:
    """
    alpha=1-신뢰도, share_left∈[0,1]. 수치안정성 확보(ε-클램프).
    """
    eps = 1e-6
    aL = alpha * (eps + (1 - 2*eps) * share_left)
    aR = alpha - aL
    zl = norm_ppf(aL)
    zr = norm_ppf(1 - aR)
    L = (zr - zl) * se
    return L, zl, zr

def draw_pdf_with_shade(zl: float, zr: float):
    xs = np.linspace(-4.5, 4.5, 700)
    pdf = 1/np.sqrt(2*np.pi)*np.exp(-xs**2/2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=pdf, mode="lines", name="N(0,1) 밀도"))
    mask = (xs >= zl) & (xs <= zr)
    if mask.any():
        fig.add_trace(go.Scatter(x=xs[mask], y=pdf[mask], fill='tozeroy', mode='lines',
                                 name="고정 면적(신뢰도)", opacity=0.5))
    fig.add_vline(x=zl, line_dash="dot", line_color="gray")
    fig.add_vline(x=zr, line_dash="dot", line_color="gray")
    fig.update_layout(height=340, xaxis_title="표준화(Z)", yaxis_title="밀도",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.02))
    return fig

# -----------------------------
# (공통) 대칭 신뢰구간 길이
# -----------------------------
def length_symmetric(alpha: float, se: float) -> float:
    return 2.0 * z(alpha/2.0) * se

# -----------------------------
# 메인
# -----------------------------
def render():
    st.sidebar.subheader("⚙️ 표본 정보")
    sigma = st.sidebar.number_input("모표준편차 σ (알고 있다고 가정)", value=10.0, step=0.5)
    n     = st.sidebar.number_input("표본 크기 n", min_value=1, value=25, step=1)
    se = float(sigma / np.sqrt(n))

    # ----------------- 파트 1 (그대로) -----------------
    st.markdown("### 1) 같은 신뢰도에서 **가장 짧은 신뢰구간**은 왜 대칭일까?")
    colA, colB = st.columns([2,1])
    with colB:
        CL = st.slider("신뢰도 (1−α)", min_value=0.50, max_value=0.999, value=0.95, step=0.001, format="%.3f")
        alpha = 1.0 - CL
        share_left = st.slider("왼쪽 꼬리 비율 (α_L/α)", 0.0, 1.0, 0.50, step=0.01)

    L, zl, zr = ci_length_asym(alpha, share_left, se)
    L_sym = length_symmetric(alpha, se)
    zl_sym, zr_sym = -z(alpha/2.0), z(alpha/2.0)

    with colA:
        st.caption("표준정규의 면적(=신뢰도)을 고정한 채로 경계를 움직여 봅니다.")
        fig = draw_pdf_with_shade(zl, zr)
        fig.add_vline(x=zl_sym, line=dict(color="purple", width=2), annotation_text="대칭 경계")
        fig.add_vline(x=zr_sym, line=dict(color="purple", width=2))
        st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("현재 구간 길이", f"{L:.4f}")
    c2.metric("대칭 구간 길이(최소)", f"{L_sym:.4f}")
    c3.metric("길이 차이(현재−대칭)", f"{(L - L_sym):.4f}")

    # 비대칭 비율별 길이 곡선
    r_eps = 1e-6
    r_grid = np.linspace(r_eps, 1-r_eps, 201)
    lengths = [ci_length_asym(alpha, r, se)[0] for r in r_grid]
    fig_len = go.Figure()
    fig_len.add_trace(go.Scatter(x=r_grid, y=lengths, mode="lines", name="길이 L(α_L/α)"))
    fig_len.add_vline(x=0.5, line_color="purple", line_dash="dash",
                      annotation_text="대칭(최소)", annotation_position="top")
    fig_len.add_vline(x=share_left, line_color="gray", line_dash="dot",
                      annotation_text="현재 비율")
    fig_len.update_layout(height=320, xaxis_title="왼쪽 꼬리 비율  α_L / α",
                          yaxis_title=f"구간 길이")
    st.plotly_chart(fig_len, use_container_width=True)

    st.divider()

    # ----------------- 파트 2 (새 설계) -----------------
    st.markdown("### 2) 신뢰도를 1%씩 올릴 때 **정확도(길이)** 는 얼마나 희생될까?")
    st.caption("대칭 신뢰구간 기준. 50%에서 시작해 1%p씩 올리며 길이 증가 ΔL과 ‘효율’=0.01/ΔL을 봅니다.")

    # 신뢰도 그리드(1% 간격). 99%에서 멈춤(끝점 100%는 분위수 무한대)
    CL_grid = np.arange(0.50, 0.99 + 1e-9, 0.01)  # 50%, 51%, ..., 99%
    alphas = 1.0 - CL_grid
    L_grid = np.array([length_symmetric(a, se) for a in alphas])

    # ΔL (다음 1%p로 올릴 때 길이 증가) : 마지막 값은 NaN
    dCL = 0.01
    dL = np.empty_like(L_grid)
    dL[:-1] = L_grid[1:] - L_grid[:-1]
    dL[-1] = np.nan

    # 효율 = ΔCL / ΔL  (ΔCL은 0.01로 고정)
    efficiency = dCL / dL
    efficiency[-1] = np.nan

    # 그래프 1: 신뢰도 vs 길이
    fig_L = go.Figure()
    fig_L.add_trace(go.Scatter(x=CL_grid, y=L_grid, mode="lines+markers", name="길이 L(CL)"))
    fig_L.add_vline(x=0.95, line_dash="dash", line_color="gray",
                    annotation_text="95%", annotation_position="top")
    fig_L.update_layout(height=320, xaxis_title="신뢰도 (1−α)", yaxis_title="구간 길이")
    st.plotly_chart(fig_L, use_container_width=True)

    # 그래프 2: 신뢰도 vs ΔL (1%p 올릴 때 추가 길이)
    fig_dL = go.Figure()
    fig_dL.add_trace(go.Scatter(x=CL_grid[:-1], y=dL[:-1], mode="lines+markers", name="ΔL(1%p 상승 시)"))
    fig_dL.add_vline(x=0.95, line_dash="dash", line_color="gray",
                     annotation_text="95%", annotation_position="top")
    fig_dL.update_layout(height=320, xaxis_title="신뢰도 (1−α)", yaxis_title="추가 길이 ΔL")
    st.plotly_chart(fig_dL, use_container_width=True)

    # 그래프 3: 신뢰도 vs 효율 = 0.01/ΔL (값이 클수록 ‘1%p 올릴 때 얻는 이득/비용’이 큼)
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Scatter(x=CL_grid[:-1], y=efficiency[:-1], mode="lines+markers", name="효율 = 0.01 / ΔL"))
    # 최대 효율 지점
    idx_max = int(np.nanargmax(efficiency[:-1]))
    cl_star = float(CL_grid[idx_max])
    y_star  = float(efficiency[idx_max])
    fig_eff.add_vline(x=0.95, line_dash="dash", line_color="gray",
                      annotation_text="95%", annotation_position="top")
    fig_eff.add_vline(x=cl_star, line_color="purple",
                      annotation_text=f"최대≈{cl_star:.2f}", annotation_position="bottom")
    fig_eff.update_layout(height=340, xaxis_title="신뢰도 (1−α)", yaxis_title="효율 = 0.01 / ΔL")
    st.plotly_chart(fig_eff, use_container_width=True)

    # 요약 카드
    a95 = 1 - 0.95
    L95 = length_symmetric(a95, se)
    # 95%에서의 ΔL과 효율
    i95 = int(round((0.95 - 0.50) / 0.01))
    dL95 = float(dL[i95]) if i95 < len(dL)-1 else float("nan")
    eff95 = float(efficiency[i95]) if i95 < len(efficiency)-1 else float("nan")

    c1, c2, c3 = st.columns(3)
    c1.metric("SE = σ/√n", f"{se:.4f}")
    c2.metric("95%의 구간 길이 L", f"{L95:.4f}")
    c3.metric("95%에서 효율(0.01/ΔL)", f"{eff95:.4f}")

    st.markdown(
        """
        **해석 가이드**  
        - **ΔL 그래프**: 신뢰도가 높아질수록 **1%p 더 올릴 때** 필요한 **추가 길이(비용)** 가 급격히 커집니다.  
        - **효율 그래프(0.01/ΔL)**: 낮은 신뢰도에서는 길이가 거의 늘지 않아 효율이 높고,  
          높은 신뢰도에서는 길이가 크게 늘어 효율이 낮아집니다.  
          많은 설정에서 **약 95% 근처**에서 효율이 **최대**가 되어 “**비용 대비 이득의 균형점**”처럼 보입니다.  
        - **n↑ 또는 σ↓(=SE↓)** 이면 전체 길이가 줄어들어 **더 높은 신뢰도**까지도 비교적 작은 ΔL로 감당할 수 있습니다.
        """
    )
