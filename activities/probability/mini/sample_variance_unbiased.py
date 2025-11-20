import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import List

PAGE_META = {
    "title": "표본분산: 왜 n-1로 나눌까?",
    "group": "확률과통계",
    "icon": "📏",
}

# ---------- 컨셉 도식(라이트 테마, 유니코드 라벨) ----------
def draw_concept_diagram() -> go.Figure:
    fig = go.Figure()
    fig.update_xaxes(visible=False, range=[0, 10])
    fig.update_yaxes(visible=False, range=[0, 6], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=260,
    )

    # 큰 타원(모집단)
    fig.add_shape(
        type="circle",
        x0=0.6, y0=1.1, x1=9.4, y1=4.9,
        line=dict(color="rgb(60,60,60)", width=2),
        fillcolor="rgba(0,0,0,0)"
    )
    fig.add_annotation(x=9.25, y=4.75, text="모집단", showarrow=False, font=dict(size=14, color="rgb(60,60,60)"))

    # 작은 타원들(표본 영역을 은은하게)
    fig.add_shape(
        type="circle",
        x0=2.2, y0=2.15, x1=7.8, y1=3.85,
        line=dict(color="rgba(120,120,120,0.9)", width=1.5),
        fillcolor="rgba(120,120,120,0.05)"
    )
    fig.add_shape(
        type="circle",
        x0=3.2, y0=2.45, x1=6.8, y1=3.55,
        line=dict(color="rgba(160,160,160,0.6)", width=1),
        fillcolor="rgba(160,160,160,0.06)"
    )
    fig.add_annotation(x=2.05, y=2.1, text="표본", showarrow=False, font=dict(size=12, color="rgb(80,80,80)"))

    # 수직 기준선(왼쪽: X̄, 오른쪽: μ)
    fig.add_shape(type="line", x0=4.0, x1=4.0, y0=1.0, y1=5.0, line=dict(color="rgba(90,90,90,0.35)", width=2))
    fig.add_shape(type="line", x0=6.2, x1=6.2, y0=1.0, y1=5.0, line=dict(color="rgba(90,90,90,0.35)", width=2))
    # ⚠️ 유니코드 사용: X̄(= 'X' + U+0304), μ
    fig.add_annotation(x=3.95, y=1.0, text="X̄", showarrow=False, font=dict(size=13, color="rgb(60,60,60)"))
    fig.add_annotation(x=6.15, y=1.0, text="μ", showarrow=False, font=dict(size=13, color="rgb(60,60,60)"))

    # 보라색 양방향 화살표: 표본들이 표본평균에서 퍼진 정도
    fig.add_annotation(x=5.15, y=3.0, ax=4.35, ay=3.0,
                       arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="rgb(204,0,204)")
    fig.add_annotation(x=4.35, y=3.0, ax=5.15, ay=3.0,
                       arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="rgb(204,0,204)")

    # 노란 화살표: 표본평균이 모평균에서 벗어난 정도
    fig.add_annotation(x=6.2, y=3.55, ax=4.0, ay=3.55,
                       arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="rgb(230,170,0)")

    # 범례 텍스트(위쪽, 배경 대비 살짝 진하게)
    fig.add_annotation(x=2.0, y=5.2, text="보라색: 표본이 표본평균에서 퍼진 정도",
                       showarrow=False, font=dict(size=11, color="rgb(204,0,204)"))
    fig.add_annotation(x=3.5, y=4.8, text="노란색: 표본평균이 모평균에서 벗어난 정도",
                       showarrow=False, font=dict(size=11, color="rgb(230,170,0)"))
    return fig

def render():
    # -------- 사이드바 --------
    st.sidebar.subheader("⚙️ 설정")
    m = st.sidebar.slider("모집단 원소의 개수", 1, 10, 4, step=1)
    default_vals = [2, 4, 6, 8] + [i for i in range(1, 11)]
    defaults = default_vals[:m]

    values: List[float] = []
    col_num = 2 if m <= 6 else 3
    cols = st.sidebar.columns(col_num)
    for i in range(m):
        with cols[i % col_num]:
            v = st.number_input(f"원소 {i+1}", value=int(defaults[i]), step=1, format="%d")
            values.append(float(v))

    n = st.sidebar.slider("표본 크기 n", 2, 50, 5, step=1)
    trials = st.sidebar.slider("시행(표본) 수", 100, 20000, 3000, step=100)
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)

    values_np = np.array(values, dtype=float)
    mu = values_np.mean()
    sigma2 = values_np.var(ddof=0)
    sigma = np.sqrt(sigma2)

    # -------- 상단: 도식 + 핵심 수식 --------
    st.markdown("## 표본분산: 왜 \\(n-1\\)로 나눌까?")
    st.plotly_chart(draw_concept_diagram(), use_container_width=True)

    st.markdown("#### 핵심 관계식")
    st.latex(
        r"""
        \underbrace{\frac{1}{n}\sum_{i=1}^n (X_i-\mu)^2}_{\text{모평균 기준 퍼짐}}
        \;=\;
        \underbrace{\frac{1}{n}\sum_{i=1}^n (X_i-\overline{X})^2}_{\text{표본평균 기준 퍼짐}}
        \;+\;
        \underbrace{(\overline{X}-\mu)^2}_{\text{표본평균의 이동}}
        """
    )
    st.latex(
        r"""
        \mathbb{E}\!\left[\frac{1}{n}\sum_{i=1}^n (X_i-\overline{X})^2\right]
        \;=\;\frac{n-1}{n}\,\sigma^2
        \quad\Rightarrow\quad
        S^2 \;=\; \frac{1}{n-1}\sum_{i=1}^n (X_i-\overline{X})^2
        \ \text{는 불편추정량}.
        """
    )

    # -------- 시뮬레이션: (1/n) vs (1/(n-1)) --------
    rng = np.random.default_rng(int(seed))
    s2_n_vals  = np.zeros(trials)   # (1/n) * sum (Xi - Xbar)^2  -> biased
    s2_n1_vals = np.zeros(trials)   # (1/(n-1)) * sum (Xi - Xbar)^2 -> unbiased

    for t in range(trials):
        sample = rng.choice(values_np, size=n, replace=True)
        xbar = sample.mean()
        s2_n_vals[t]  = np.mean((sample - xbar) ** 2)
        s2_n1_vals[t] = np.var(sample, ddof=1)

    # 히스토그램(겹침)
    fig_hist = go.Figure()
    fig_hist.add_histogram(x=s2_n_vals,  name="(1/n)·Σ(Xᵢ−X̄)²",  opacity=0.55)
    fig_hist.add_histogram(x=s2_n1_vals, name="(1/(n−1))·Σ(Xᵢ−X̄)²", opacity=0.55)
    fig_hist.add_vline(y0=0, y1=1, x=sigma2, line_dash="dash", line_width=2,
                       annotation_text=f"모분산 σ²={sigma2:.4f}")
    fig_hist.update_layout(barmode="overlay", xaxis_title="추정값", yaxis_title="빈도", height=380)
    st.markdown("### 분산 추정량 분포 비교")
    st.plotly_chart(fig_hist, use_container_width=True)

    # 누적 평균(수렴)
    cum_mean_n  = np.cumsum(s2_n_vals)  / np.arange(1, trials + 1)
    cum_mean_n1 = np.cumsum(s2_n1_vals) / np.arange(1, trials + 1)
    fig_cum = go.Figure()
    fig_cum.add_scatter(y=cum_mean_n,  mode="lines", name="(1/n) 평균")
    fig_cum.add_scatter(y=cum_mean_n1, mode="lines", name="(1/(n−1)) 평균")
    fig_cum.add_hline(y=sigma2, line_dash="dash", line_width=2,
                      annotation_text=f"모분산 σ²={sigma2:.4f}")
    fig_cum.update_layout(xaxis_title="시행 수(누적)", yaxis_title="누적 평균", height=380)
    st.plotly_chart(fig_cum, use_container_width=True)

    # 요약
    st.markdown("### 요약")
    c1, c2, c3 = st.columns(3)
    c1.metric("모분산 σ²", f"{sigma2:.6f}")
    c2.metric("평균[(1/n)·Σ(Xᵢ−X̄)²]",  f"{s2_n_vals.mean():.6f}")
    c3.metric("평균[(1/(n−1))·Σ(Xᵢ−X̄)²]", f"{s2_n1_vals.mean():.6f}")

    st.markdown(
        "- **(1/n)** 으로 나누면 평균이 보통 **σ²보다 작게** 나옵니다(편향).  \n"
        "- **(1/(n−1))** 는 평균이 **σ²에 수렴**하여 불편추정량이 됩니다."
    )
