import streamlit as st
import numpy as np
import plotly.express as px
from utils import set_base_page, page_header

set_base_page("원주율 추정 (몬테카를로)", "📐")
page_header("원주율 추정 (몬테카를로)", "단위 정사각형에 무작위 점 찍기 → 원 내부 비율로 π 근사")

st.sidebar.subheader("⚙️ 설정")
N = st.sidebar.slider("무작위 점 개수", 100, 200000, 5000, step=100)

rng = np.random.default_rng()
x = rng.random(N)
y = rng.random(N)
inside = (x**2 + y**2) <= 1.0
pi_est = 4 * inside.mean()

st.metric("π 추정값", f"{pi_est:.6f}", delta=f"{pi_est - np.pi:+.6f}")

sample = min(N, 8000)  # 렌더링 부담 완화
fig = px.scatter(
    x=x[:sample], y=y[:sample],
    color=inside[:sample],
    labels={"x": "x", "y": "y", "color": "원 내부 여부"},
    title="무작위 점 산포도 (표본 일부 시각화)"
)
fig.update_traces(marker=dict(size=4, opacity=0.7))
st.plotly_chart(fig, use_container_width=True)

st.caption("점 개수가 커질수록 추정값이 안정됩니다. (표본 평균의 수렴)")
