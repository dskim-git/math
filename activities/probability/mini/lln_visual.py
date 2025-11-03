import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Tuple

PAGE_META = {
    "title": "큰 수의 법칙 시각화",
    "group": "확률과통계",
    "icon": "📚",
}

# --------- 샘플 생성기 ---------
def sample_generator(dist: str, n: int, params: dict, rng: np.random.Generator) -> np.ndarray:
    if dist == "베르누이":
        p = params.get("p", 0.5)
        return rng.binomial(1, p, size=n).astype(float)
    elif dist == "정규분포":
        mu = params.get("mu", 0.0); sigma = max(1e-9, params.get("sigma", 1.0))
        return rng.normal(mu, sigma, size=n)
    elif dist == "균등분포[0,1]":
        return rng.random(n)
    else:
        # 안전장치
        return rng.random(n)

def true_mean(dist: str, params: dict) -> float:
    if dist == "베르누이":
        return params.get("p", 0.5)
    elif dist == "정규분포":
        return params.get("mu", 0.0)
    elif dist == "균등분포[0,1]":
        return 0.5
    return 0.0

# --------- UI / 메인 렌더 ---------
def render():
    st.sidebar.subheader("⚙️ 분포 선택 & 파라미터")
    dist = st.sidebar.selectbox("분포", ["베르누이", "정규분포", "균등분포[0,1]"])

    params = {}
    if dist == "베르누이":
        params["p"] = st.sidebar.slider("성공확률 p", 0.0, 1.0, 0.5, 0.01)
    elif dist == "정규분포":
        col1, col2 = st.sidebar.columns(2)
        params["mu"] = col1.number_input("μ", value=0.0, step=0.1)
        params["sigma"] = max(1e-9, col2.number_input("σ (>0)", value=1.0, step=0.1, min_value=0.01))
    # 균등분포[0,1]은 파라미터 없음

    st.sidebar.subheader("🎛️ 실험 설정")
    max_n = st.sidebar.slider("최대 표본 크기 n (경로 길이)", 50, 5000, 1000, step=50)
    paths = st.sidebar.slider("경로(반복) 수", 1, 200, 50, step=1)
    eps = st.sidebar.number_input("ε (허용 오차)", value=0.1, min_value=0.0, step=0.01, format="%.2f")
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)

    st.sidebar.subheader("🔎 비교 기준")
    show_seq_def = st.sidebar.checkbox("수열 극한 정의(∀ε, ∃N, ∀n≥N)와 비교 설명 보이기", value=True)

    mu = true_mean(dist, params)

    st.markdown("### 큰 수의 법칙(LLN): *표본평균*이 모평균으로 확률적으로 수렴")
    st.caption(
        "표본평균 "
        " $\\overline{X}_n = \\frac{1}{n}\\sum_{i=1}^n X_i$ "
        " 가 $n \\to \\infty$ 일 때 $\\mu$로 **확률적으로 수렴**한다는 것은, "
        "고정된 임의의 $\\varepsilon>0$에 대해 $\\mathsf{P}(|\\overline{X}_n-\\mu|<\\varepsilon) \\to 1$ 을 뜻합니다."
    )

    # --------- 시뮬레이션 ---------
    rng = np.random.default_rng(int(seed))
    # 모든 경로에 대해 누적평균 경로를 만든다: shape (paths, max_n)
    Xbars = np.zeros((paths, max_n), dtype=float)
    inside = np.zeros((paths, max_n), dtype=bool)

    for k in range(paths):
        x = sample_generator(dist, max_n, params, rng)
        csum = np.cumsum(x)
        xbar = csum / np.arange(1, max_n + 1)
        Xbars[k, :] = xbar
        inside[k, :] = np.abs(xbar - mu) < eps

    # n별로 밴드 안에 들어온 경로 비율
    prop_inside = inside.mean(axis=0)  # length max_n

    # --------- 그림 1: 여러 경로의 표본평균 수렴 모습 ---------
    fig1 = go.Figure()
    # 몇 개만 진하게, 나머지는 얇게 표시 (렌더링 성능/가독성)
    strong = min(8, paths)
    for i in range(paths):
        width = 2 if i < strong else 1
        opacity = 0.9 if i < strong else 0.35
        fig1.add_scatter(
            x=np.arange(1, max_n + 1),
            y=Xbars[i],
            mode="lines",
            line=dict(width=width),
            opacity=opacity,
            showlegend=False
        )

    # μ 기준선 & ε-밴드
    fig1.add_hline(y=mu, line_width=2, line_dash="dash", annotation_text=f"μ = {mu:.3f}")
    if eps > 0:
        fig1.add_hline(y=mu + eps, line_width=1, line_dash="dot")
        fig1.add_hline(y=mu - eps, line_width=1, line_dash="dot")
        fig1.add_shape(
            type="rect",
            x0=1, x1=max_n,
            y0=mu - eps, y1=mu + eps,
            fillcolor="LightSkyBlue", opacity=0.15, line_width=0, layer="below"
        )

    fig1.update_layout(
        title=f"표본평균 경로들: LLN의 직관 (분포={dist}, 경로={paths}개, 최대 n={max_n}, ε={eps})",
        xaxis_title="n (누적 표본 크기)",
        yaxis_title="표본평균 ȳₙ",
        hovermode="x unified"
    )

    # --------- 그림 2: P(|ȳₙ-μ|<ε)의 경험적 추정 (n에 따른 증가) ---------
    fig2 = go.Figure()
    fig2.add_scatter(
        x=np.arange(1, max_n + 1),
        y=prop_inside,
        mode="lines",
        line=dict(width=3),
        name="경험적 확률"
    )
    fig2.update_layout(
        title="n에 따른  P(|ȳₙ − μ| < ε)  (시뮬레이션 경로 비율)",
        xaxis_title="n",
        yaxis_title="비율 (경험적 확률)",
        yaxis=dict(range=[0, 1.0])
    )

    # --------- 인터랙션: 특정 n에서 '얼마나 많은 경로가 밴드 안?' ---------
    st.plotly_chart(fig1, use_container_width=True)
    n_check = st.slider("🔍 특정 n에서 밴드 안의 경로 비율을 확인해 보세요", 1, max_n, int(0.6*max_n), step=1)
    st.info(f"n = {n_check} 에서  |ȳₙ − μ| < ε  인 경로 비율(추정치): **{prop_inside[n_check-1]:.3f}**  "
            f"(경로 수 {paths} 중 {int(prop_inside[n_check-1]*paths)}개)")

    st.plotly_chart(fig2, use_container_width=True)

    # --------- 개념 비교(수열 극한 vs LLN) ---------
    if show_seq_def:
        st.markdown("### 왜 ‘수열 극한’보다 약하게(확률적으로) 표현할까?")
        st.markdown(
            """
**수열의 극한 정의**는  
> 임의의 $\\varepsilon>0$에 대해, 어떤 $N$이 존재하여 **모든** $n\\ge N$에 대해 $|a_n-L|<\\varepsilon$.

반면 **큰 수의 법칙(확률적 수렴)**은  
> 임의의 $\\varepsilon>0$에 대해, $\\mathsf{P}(|\\overline{X}_n-\\mu|<\\varepsilon)\\to 1$.

즉,
- 수열 극한: 한 **결정적(확정적)** 수열에 대해, 충분히 큰 이후에는 **영원히** $\\varepsilon$-밴드 안에 머물러야 합니다.  
- LLN: 각각의 시행(표본 경로)이 **우연성**을 가지므로, 모든 경로가 동시에 영원히 밴드 안에 들어간다고 보장할 수는 없지만,  
  **그럴 확률이 1에 가까워진다**고 말합니다.

위의 첫 번째 그래프에서 개별 경로(얇은 여러 곡선)는 때때로 밴드 밖으로 **튀어나왔다가** 다시 들어오곤 합니다.  
하지만 두 번째 그래프에서 보듯이, 표본 크기 $n$이 커질수록 **대부분의 경로가 밴드 안에 있게 되는 비율**은 1에 가까워집니다.
            """
        )

    with st.expander("📎 (선택) 원자료/추가 지표 보기"):
        # 마지막 n에서 경로별 오차 분포
        err_last = np.abs(Xbars[:, -1] - mu)
        st.write(f"마지막 n={max_n}에서 |ȳₙ−μ|의 요약 통계:")
        st.write({
            "평균오차": float(err_last.mean()),
            "중앙값": float(np.median(err_last)),
            "90%분위": float(np.quantile(err_last, 0.9)),
        })
        st.plotly_chart(px.histogram(err_last, nbins=20, title=f"|ȳₙ−μ| 분포 (n={max_n})"),
                        use_container_width=True)

    st.caption("팁: ε을 작게 하고 n을 키워 보세요. 두 번째 그래프(비율 곡선)가 1에 더 가까워집니다.")
