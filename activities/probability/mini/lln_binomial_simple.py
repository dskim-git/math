import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

PAGE_META = {
    "title": "큰 수의 법칙(이항·심플)",
    "group": "확률과통계",
    "icon": "🎯",
}

def _compute_n_star_per_path(ratios: np.ndarray, p: float, eps: float):
    """
    경로별 Big-N (N*): 그 시점 이후로는 밴드(|ratio - p| < eps)를 절대 벗어나지 않게 되는
    '최소의 N'을 계산.
    - ratios: shape (paths, n_max), 각 행이 한 경로의 상대도수 시퀀스 X_n/n
    반환: list[Optional[int]]  (1-indexed N*, 없으면 None)
    """
    paths, n_max = ratios.shape
    Nstars = []
    outside_all = np.abs(ratios - p) >= eps  # True면 밴드 바깥
    for i in range(paths):
        outs = outside_all[i]
        if not outs.any():
            # 처음부터 끝까지 한 번도 벗어나지 않음 → N*=1
            Nstars.append(1)
            continue
        last_out_idx = np.where(outs)[0].max()
        if last_out_idx == n_max - 1:
            # 관측 종료 시점(n_max)에서도 여전히 바깥 → 그 이후는 미정
            Nstars.append(None)
        else:
            # 마지막 바깥이 n = last_out_idx+1 이므로, 그 다음 n부터는 항상 안쪽
            Nstars.append(last_out_idx + 2)
    return Nstars

def render():
    st.sidebar.subheader("⚙️ 파라미터")
    p = st.sidebar.slider("수학적 확률 p (성공확률)", 0.0, 1.0, 0.5, 0.01)
    n_max = st.sidebar.slider("시행 횟수 n (최대)", 50, 5000, 800, step=50)
    paths = st.sidebar.slider("경로(반복) 수", 1, 50, 10, step=1)  # 범위/기본값 수정
    eps = st.sidebar.number_input("ε (허용 오차)", value=0.1, min_value=0.0, step=0.01, format="%.2f")
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)
    show_bound = st.sidebar.checkbox("체비셰프 상계선(선택) 표시", value=False)
    show_Nstar = st.sidebar.checkbox("경로별 N* 표시", value=True)  # N* 토글

    st.markdown("### 이항 시뮬레이션으로 보는 큰 수의 법칙")
    st.caption(
        r"베르누이 시행을 $n$번 했을 때 $X_n$=성공 횟수, 상대도수 $\frac{X_n}{n}$ 은 "
        r"수학적 확률 $p$ 에 **확률적으로 수렴**합니다."
    )

    rng = np.random.default_rng(int(seed))
    ratios = np.zeros((paths, n_max))
    for k in range(paths):
        x = rng.binomial(1, p, size=n_max).astype(float)
        csum = np.cumsum(x)
        ratios[k] = csum / np.arange(1, n_max + 1)

    # n별 밴드 안 비율
    inside = np.abs(ratios - p) < eps
    prop_inside = inside.mean(axis=0)

    # --- 경로별 N* 계산 ---
    Nstars = _compute_n_star_per_path(ratios, p, eps)

    # ---------- 그림 1: 여러 경로의 상대도수 & N* 표시 ----------
    fig1 = go.Figure()
    strong = min(8, paths)  # 몇 개는 굵게
    x_axis = np.arange(1, n_max + 1)

    for i in range(paths):
        width = 2 if i < strong else 1
        opacity = 0.9 if i < strong else 0.35
        fig1.add_scatter(
            x=x_axis,
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

    # 경로별 N* 마커/보조선 표시 (너무 복잡해지지 않도록 마커만, 상위 몇 개는 주석 포함)
    if show_Nstar:
        for i, Nstar in enumerate(Nstars):
            if Nstar is None or Nstar > n_max:
                continue
            yN = ratios[i, Nstar - 1]
            # 마커
            fig1.add_scatter(
                x=[Nstar], y=[yN],
                mode="markers+text" if i < strong else "markers",
                marker=dict(size=9, symbol="x"),
                text=[f"N*={Nstar}"] if i < strong else None,
                textposition="top center",
                showlegend=False,
                opacity=0.95 if i < strong else 0.6
            )
            # (선택) 세로 보조선은 복잡해질 수 있어 기본 비활성화
            # fig1.add_vline(x=Nstar, line_width=1, line_dash="dot", opacity=0.2)

    fig1.update_layout(
        title="상대도수 Xₙ/n 의 경로들 (+ 경로별 N*)",
        xaxis_title="시행 횟수 n",
        yaxis_title="상대도수 Xₙ/n",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ---------- 특정 n에서 밴드 안 비율 ----------
    n_check = st.slider("🔍 특정 n에서 |Xₙ/n − p| < ε 인 경로 비율", 1, n_max, int(0.6 * n_max), step=1)
    st.info(
        f"n = {n_check} 에서  |Xₙ/n − p| < ε  비율: **{prop_inside[n_check-1]:.3f}**  "
        f"(경로 {paths}개 중 {int(prop_inside[n_check-1]*paths)}개)"
    )

    # ---------- 그림 2: n에 따른 비율 곡선 ----------
    fig2 = go.Figure()
    fig2.add_scatter(
        x=x_axis,
        y=prop_inside,
        mode="lines",
        line=dict(width=3),
        name="경험적 비율"
    )

    # 선택: 체비셰프 하한(이론)
    if show_bound and eps > 0:
        upper = 1 - (p * (1 - p)) / (x_axis * (eps ** 2))
        upper = np.clip(upper, 0, 1)
        fig2.add_scatter(
            x=x_axis, y=upper, mode="lines", line=dict(width=2, dash="dash"),
            name="체비셰프: 하한(이론)"
        )

    fig2.update_layout(
        title="n에 따른  P(|Xₙ/n − p| < ε)  (시뮬레이션 경로 비율)",
        xaxis_title="n",
        yaxis_title="비율",
        yaxis=dict(range=[0, 1.0])
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ---------- 개념 비교 ----------
    with st.expander("📘 수열의 극한 vs 큰 수의 법칙(확률적 수렴) 간단 비교"):
        st.markdown(
            r"""
**수열의 극한(결정적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, 어떤 $N$이 있어 **모든** $n\ge N$에 대해 $|a_n-L|<\varepsilon$.

**큰 수의 법칙(확률적 수렴)**  
- 임의의 $\varepsilon>0$에 대해, $n\to\infty$ 이면  
  $\mathsf{P}(|X_n/n - p|<\varepsilon)\to 1$.

👉 이 페이지의 N* 표시는 “**수열의 극한에선 고정된 N이 하나**”지만,  
**확률적 수렴에선 경로마다 N*가 다를 수 있음**을 시각적으로 보여줍니다.  
관측 한계 때문에 어떤 경로는 N*가 **미정(> n_{\max})**일 수도 있어요.
"""
        )

    with st.expander("📎 (선택) 경로별 N* 요약"):
        data = []
        for i, Nstar in enumerate(Nstars, start=1):
            data.append({"경로": i, "N*": ("미정(>n_max)" if Nstar is None else int(Nstar))})
        st.dataframe(data, use_container_width=True)

    st.caption("Tip: ε을 줄이면 N*가 커지는 경향을 관찰할 수 있어요. 경로 수는 10~20 내로 두면 시각적으로 깔끔합니다.")
