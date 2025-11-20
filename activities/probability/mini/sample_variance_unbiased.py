import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

PAGE_META = {
    "title": "표본분산: 왜 n-1로 나눌까?",
    "group": "확률과통계",
    "icon": "📏",
}

def render():
    # -------- 사이드바(간단 조작) --------
    st.sidebar.subheader("⚙️ 설정")
    m = st.sidebar.slider("모집단 원소의 개수", 1, 10, 4, step=1)
    default_vals = [2, 4, 6, 8] + [i for i in range(1, 11)]
    defaults = default_vals[:m]

    values = []
    col_num = 2 if m <= 6 else 3
    cols = st.sidebar.columns(col_num)
    for i in range(m):
        with cols[i % col_num]:
            v = st.number_input(f"원소 {i+1}", value=int(defaults[i]), step=1, format="%d")
            values.append(int(v))

    n = st.sidebar.slider("표본 크기 n", 2, 50, 5, step=1)  # n=1이면 분산 정의 어려워서 2부터
    trials = st.sidebar.slider("시행(표본) 수", 100, 20000, 3000, step=100)
    seed = st.sidebar.number_input("난수 시드", value=0, step=1)

    values = np.array(values, dtype=float)
    mu = values.mean()
    sigma2 = values.var(ddof=0)
    sigma = np.sqrt(sigma2)

    st.markdown("## 표본분산: 왜 \\(n-1\\)인가?")
    st.caption("복원추출로 표본을 반복해 뽑아 보며, 분해식과 편향(bias)을 동시에 확인합니다.")

    # -------- 상단: ‘분해식’ 안내(이미지 컨셉 연결) --------
    with st.expander("📘 핵심 분해식 보기 (그림과 같은 구조)", expanded=True):
        st.latex(
            r"""
            \underbrace{\frac{1}{n}\sum_{i=1}^n (X_i-\mu)^2}_{\text{표본들이 모평균에서 퍼진 정도}}
            \;=\;
            \underbrace{\frac{1}{n}\sum_{i=1}^n (X_i-\overline{X})^2}_{\text{표본들이 표본평균에서 퍼진 정도}}
            \;+\;
            \underbrace{(\overline{X}-\mu)^2}_{\text{표본평균이 모평균에서 퍼진 정도}}
            """
        )
        st.markdown(
            "- 왼쪽(흰색 타원): 표본들을 **모평균**으로부터 본 퍼짐\n"
            "- 보라색 타원: 표본들을 **표본평균**으로부터 본 퍼짐\n"
            "- 노란 화살표: **표본평균**이 모평균에서 벗어난 정도\n\n"
            "양변의 **기댓값**을 취하면\n"
            r"\(\; \mathbb{E}\!\left[\tfrac{1}{n}\sum (X_i-\overline{X})^2\right] = \frac{n-1}{n}\sigma^2 \;\)"
            "이 되어, **\\(n\\)**으로 나누면 평균적으로 **작게** 나옵니다. "
            "그래서 **\\(n-1\\)**로 나눈 "
            r"\(S^2=\tfrac{1}{n-1}\sum (X_i-\overline{X})^2\) 가 **불편추정량**입니다."
        )

    # -------- 시뮬레이션 --------
    rng = np.random.default_rng(int(seed))
    Xbars = np.zeros(trials)
    s2_n   = np.zeros(trials)  # (1/n) * sum (Xi - Xbar)^2  -> biased
    s2_n1  = np.zeros(trials)  # (1/(n-1)) * sum (Xi - Xbar)^2  -> unbiased
    lhs_n  = np.zeros(trials)  # (1/n) * sum (Xi - mu)^2
    rhs_n  = np.zeros(trials)  # (1/n) * sum (Xi - Xbar)^2 + (Xbar - mu)^2

    for t in range(trials):
        sample = rng.choice(values, size=n, replace=True)
        xbar = sample.mean()
        Xbars[t] = xbar
        s2_n[t]  = np.mean((sample - xbar)**2)
        s2_n1[t] = np.var(sample, ddof=1)      # = sum(...)/(n-1)
        lhs_n[t] = np.mean((sample - mu)**2)
        rhs_n[t] = s2_n[t] + (xbar - mu)**2

    # -------- 분해식 확인(한눈에) --------
    diff = lhs_n - rhs_n
    st.markdown("### 분해식 체크:  \\(\\tfrac{1}{n}\\sum (X_i-\\mu)^2 = \\tfrac{1}{n}\\sum (X_i-\\overline{X})^2 + (\\overline{X}-\\mu)^2\\)")
    st.caption("각 시행에서 좌변-우변의 차이를 그립니다. 수치 오차 때문에 0 근처의 작은 값들이 나옵니다.")
    fig_diff = px.histogram(diff, nbins=40)
    fig_diff.update_layout(xaxis_title="좌변 − 우변", yaxis_title="빈도", bargap=0.05)
    st.plotly_chart(fig_diff, use_container_width=True)

    # -------- 추정량 분포(히스토그램) --------
    st.markdown("### 분산 추정량의 분포 비교")
    tabs = st.tabs(["히스토그램", "누적 평균(수렴)"])
    with tabs[0]:
        df_hist = {
            "with n": s2_n,
            "with n-1": s2_n1,
        }
        figA = go.Figure()
        figA.add_histogram(x=df_hist["with n"], opacity=0.55, name="(1/n)·Σ(Xi-X̄)²")
        figA.add_histogram(x=df_hist["with n-1"], opacity=0.55, name="(1/(n-1))·Σ(Xi-X̄)²")
        figA.add_vline(x=sigma2, line_dash="dash", line_width=2,
                       annotation_text=f"σ²(진짜)={sigma2:.4f}")
        figA.update_layout(barmode="overlay", xaxis_title="추정값", yaxis_title="빈도")
        st.plotly_chart(figA, use_container_width=True)

    with tabs[1]:
        cum_mean_n   = np.cumsum(s2_n)  / np.arange(1, trials+1)
        cum_mean_n1  = np.cumsum(s2_n1) / np.arange(1, trials+1)
        figB = go.Figure()
        figB.add_scatter(y=cum_mean_n,  mode="lines", name="(1/n) 평균")
        figB.add_scatter(y=cum_mean_n1, mode="lines", name="(1/(n-1)) 평균")
        figB.add_hline(y=sigma2, line_dash="dash", line_width=2,
                       annotation_text=f"σ²(진짜)={sigma2:.4f}")
        figB.update_layout(xaxis_title="시행 수(누적)", yaxis_title="누적 평균")
        st.plotly_chart(figB, use_container_width=True)

    # -------- 요약 카드 --------
    st.markdown("### 요약")
    c1, c2, c3 = st.columns(3)
    c1.metric("진짜 분산 σ²", f"{sigma2:.6f}")
    c2.metric("평균[(1/n)·Σ(Xi-X̄)²]", f"{s2_n.mean():.6f}")
    c3.metric("평균[(1/(n-1))·Σ(Xi-X̄)²]", f"{s2_n1.mean():.6f}")

    st.markdown(
        """
        - **(1/n)** 으로 나눈 값의 평균은 보통 **σ²보다 작게** 수렴합니다 (편향 ⬇️).
        - **(1/(n−1))** 로 나눈 값의 평균은 **σ²에 정확히 수렴**합니다 (불편추정량 ✅).
        """
    )

    # -------- 한 줄 해설 --------
    with st.expander("수학적 한 줄 해설"):
        st.latex(
            r"""
            \mathbb{E}\!\left[\frac{1}{n}\sum (X_i-\overline{X})^2\right]
            = \frac{n-1}{n}\sigma^2
            \quad\Rightarrow\quad
            \mathbb{E}\!\left[\frac{1}{n-1}\sum (X_i-\overline{X})^2\right]=\sigma^2.
            """
        )
        st.markdown(
            "즉, 표본평균을 썼기 때문에 자유도가 1 감소해서 **분모에 (n−1)** 이 들어갑니다."
        )
