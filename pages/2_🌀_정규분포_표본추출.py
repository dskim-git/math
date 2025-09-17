import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from utils import set_base_page, page_header

set_base_page("정규분포 표본추출", "🌀")
page_header("정규분포 표본추출", "표본 히스토그램 vs 이론 밀도, 표본평균 관찰")

st.sidebar.subheader("⚙️ 매개변수")
mu = st.sidebar.number_input("모평균 μ", value=0.0, step=0.1)
sigma = st.sidebar.number_input("모표준편차 σ (>0)", value=1.0, step=0.1, min_value=0.01)
n = st.sidebar.slider("표본 크기 n", 10, 20000, 1000)
bins = st.sidebar.slider("히스토그램 구간 수", 10, 100, 40)

rng = np.random.default_rng()
x = rng.normal(mu, sigma, size=n)

# 히스토그램 (확률밀도 정규화)
hist_y, hist_x = np.histogram(x, bins=bins, density=True)
centers = 0.5 * (hist_x[:-1] + hist_x[1:])

# 이론 곡선
xs = np.linspace(min(x.min(), mu - 4*sigma), max(x.max(), mu + 4*sigma), 400)
pdf = norm.pdf(xs, loc=mu, scale=sigma)

fig = go.Figure()
fig.add_bar(x=centers, y=hist_y, name="표본 히스토그램(밀도)", opacity=0.7)
fig.add_scatter(x=xs, y=pdf, name="이론 밀도", mode="lines", line=dict(width=2))
fig.update_layout(title="정규분포 표본과 이론 밀도", xaxis_title="값", yaxis_title="밀도")
st.plotly_chart(fig, use_container_width=True)

st.write(f"표본평균: **{np.mean(x):.4f}**, 표본표준편차: **{np.std(x, ddof=1):.4f}**  (모수: μ={mu}, σ={sigma})")

with st.expander("🎯 확률 계산 (P(a ≤ X ≤ b))"):
    a, b = st.columns(2)
    a_val = a.number_input("a", value=float(mu - sigma))
    b_val = b.number_input("b", value=float(mu + sigma))
    if a_val <= b_val:
        prob = norm.cdf(b_val, mu, sigma) - norm.cdf(a_val, mu, sigma)
        st.success(f"P({a_val} ≤ X ≤ {b_val}) = **{prob:.4f}**")
    else:
        st.error("a ≤ b 를 만족하도록 값을 입력해주세요.")
