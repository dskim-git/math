import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

PAGE_META = {
    "title": "큰 수의 법칙(이항·심플)",
    "group": "확률과통계",
    "icon": "🎯",
}

def render():
    st.sidebar.subheader("⚙️ 파라미터")
    p = st.sidebar.slider("수학적 확률 p (성공확률)", 0.0, 1.0, 0.5, 0.01)
    n_max = st.sidebar.slider("시행 횟수 n (최대)", 50, 5000, 800, step=50)
    paths = st.sidebar.slider("경로(반복) 수", 1, 200, 40, step=1)
    eps = st.sidebar.number_input("ε (허용 오차)", value=0.1, min_value=0.0, step=0.01, format="%.2f")
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)
    show_bound = st.sidebar.checkbox("체비셰프 상계선(선택) 표시", value=False)

    st.markdown("### 이항 시뮬레이션으로 보는 큰 수의 법칙")
    st.caption(
        r"한 번의 시행에서 성공이면 1, 실패면 0인 베르누이 시행을 $n$번 했을 때, "
        r"$X_n$ = 성공 횟수. 통계적 확률 $\frac{X_n}{n}$ 은 수학적 확률 $p$ 에 **확률적으로 수렴**합니다."
    )

    rng = np.random.default_rng(int(seed))
    # 각 경로별로 베르누이 샘플을 누적하고 X_n/n 곡선을 만든다.
    ratios = np.zeros((paths, n_max))
    for k in range(paths):
        x = rng.binomial(1, p, size=n_max).astype(float)
        csum = np.cumsum(x)
        ratios[k] = csum / np.arange(1, n_max + 1)

    # n별로 |X_n/n - p| < eps 인 경로 비율을 계산
    inside = np.abs(ratios - p) < eps
    prop_inside = inside.mean(axis=0)

    # ---------- 그림 1: 여러 경로의 상대도수 X_n/n vs p ----------
    fig1 = go.Figure()
    strong = min(8, paths)  # 몇 개는 굵게
    for i in range(paths):
        width = 2 if i < strong else 1
        opacity = 0.9 if i < strong else 0.35
        fig1.add_scatter(
            x=np.arange(1, n_max + 1),
            y=ratios[i],
            mode="lines",
            line=dict(width=width),
            opacity=opacity,
            showlegend=False
        )

    # p 기준선 & ε-밴드
    fig1.add_hline(y=p, line_width=2, line_dash="dash", annotation_text=f"p = {p:.2f}")
    if eps > 0:
        fig1.add_hline(y=p + eps, line_width=1, line_dash="dot")
        fig1.add_hline(y=p - eps, line_width=1, line_dash="dot")
        fig1.add_shape(
            type="rect",
            x0=1, x1=n_max,
            y0=p - eps, y1=p + eps,
            fillcolor="LightSkyBlue", opacity=0.18, line_width=0, layer="below"
        )

    fig1.update_layout(
        title="상대도수 Xₙ/n 의 경로들 (여러 번의 실험을 겹쳐 그린 그래프)",
        xaxis_title="시행 횟수 n",
        yaxis_title="상대도수 Xₙ/n",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ---------- 특정 n에서 밴드 안 비율 읽기 ----------
    n_check = st.slider("🔍 특정 n에서 |Xₙ/n − p| < ε 인 경로 비율", 1, n_max, int(0.6 * n_max), step=1)
    st.info(
        f"n = {n_check} 에서  |Xₙ/n − p| < ε  비율: **{prop_inside[n_check-1]:.3f}**  "
        f"(경로 {paths}개 중 {int(prop_inside[n_check-1]*paths)}개)"
    )

    # ---------- 그림 2: n에 따른 비율 P(|Xₙ/n − p| < ε)의 경험적 추정 ----------
    fig2 = go.Figure()
    fig2.add_scatter(
        x=np.arange(1, n_max + 1),
        y=prop_inside,
        mode="lines",
        line=dict(width=3),
        name="경험적 비율"
    )

    # 선택: 체비셰프 상계 (Var(X_n/n)=p(1-p)/n → P(|.|≥ε) ≤ p(1-p)/(n ε²))
    # ⇒ P(|.|<ε) ≥ 1 − p(1-p)/(n ε²)  (0~1 범위로 잘라줌)
    if show_bound and eps > 0:
        n_arr = np.arange(1, n_max + 1)
        upper = 1 - (p * (1 - p)) / (n_arr * (eps ** 2))
        upper = np.clip(upper, 0, 1)
        fig2.add_scatter(
            x=n_arr, y=upper, mode="lines", line=dict(width=2, dash="dash"),
            name="체비셰프: 하한(이론상)"
        )

    fig2.update_layout(
        title="n에 따른  P(|Xₙ/n − p| < ε)  (시뮬레이션 경로 비율)",
        xaxis_title="n",
        yaxis_title="비율",
        yaxis=dict(range=[0, 1.0])
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ---------- 결정적 수렴(수열 극한) vs 확률적 수렴(LLN) 비교 ----------
    with st.expander("📘 수열의 극한 vs 큰 수의 법칙(확률적 수렴) 간단 비교"):
        st.markdown(
            r"""
**수열의 극한(결정적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, 어떤 $N$이 있어 **모든** $n\ge N$에 대해 $|a_n-L|<\varepsilon$.

**큰 수의 법칙(확률적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, $n\to\infty$ 이면  
  $\mathsf{P}(|X_n/n - p|<\varepsilon)\to 1$.

👉 개별 경로(상대도수 곡선)는 우연 때문에 가끔 밴드 밖으로 **튀어나올 수** 있어요.  
하지만 시행 수가 커질수록 **그 안에 들어올 확률이 1에 가까워진다**는 의미입니다.
"""
        )

    st.caption("Tip: ε을 줄여보거나 p를 바꿔가며, 두 번째 그래프(비율 곡선)가 어떻게 1에 가까워지는지 비교해 보세요.")
