import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import set_base_page, page_header

set_base_page("랜덤워크 시각화", "🚶")
page_header("2D 랜덤워크", "무작위 보행 경로와 최종 위치 분포")

st.sidebar.subheader("⚙️ 설정")
steps = st.sidebar.slider("걸음 수", 10, 5000, 500)
paths = st.sidebar.slider("경로 개수(표시)", 1, 50, 5)
show_end_dist = st.sidebar.checkbox("최종 위치 분포(반경) 보기", True)

rng = np.random.default_rng(0)
angles = rng.uniform(0, 2*np.pi, size=(paths, steps))
dx = np.cos(angles)
dy = np.sin(angles)
x = dx.cumsum(axis=1)
y = dy.cumsum(axis=1)

fig = go.Figure()
for i in range(paths):
    fig.add_scatter(x=np.r_[0, x[i]], y=np.r_[0, y[i]], mode="lines", name=f"경로 {i+1}", opacity=0.8)
fig.update_layout(title=f"2D 랜덤워크 (경로 {paths}개, 걸음 {steps}회)", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig, use_container_width=True)

if show_end_dist:
    r = np.sqrt(x[:, -1]**2 + y[:, -1]**2)
    st.write(f"마지막 반경 평균: **{r.mean():.3f}**, 표준편차: **{r.std(ddof=1):.3f}**")
    import plotly.express as px
    st.plotly_chart(px.histogram(r, nbins=20, title="최종 위치 반경 분포"),
                    use_container_width=True)
