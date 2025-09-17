import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import binom
from utils import set_base_page, page_header

set_base_page("확률 시뮬레이터", "📊")
page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교")

st.sidebar.subheader("⚙️ 실험 설정")
mode = st.sidebar.selectbox("실험 종류", ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"])
n = st.sidebar.slider("1회 실험 시행 수 (n)", 1, 200, 30)
repeats = st.sidebar.slider("반복 횟수 (시뮬레이션 반복)", 100, 20000, 3000, step=100)

if mode == "동전 던지기(공정)":
    p = 0.5
    label = "앞면(성공)"
elif mode == "주사위(특정 눈)":
    face = st.sidebar.number_input("성공 눈 (1~6)", min_value=1, max_value=6, value=6, step=1)
    p = 1/6
    label = f"{face} 눈"
else:
    p = st.sidebar.slider("성공확률 p", 0.0, 1.0, 0.35, 0.01)
    label = "성공"

st.write(f"**성공 조건:** {label} | **성공확률 p:** {p:.3f}")

# 시뮬레이션
rng = np.random.default_rng()
# (repeats, n) 베르누이 시뮬레이션 후 각 시행에서 성공 개수 합
sim = rng.binomial(n=n, p=p, size=repeats)
vals, counts = np.unique(sim, return_counts=True)
emp_prob = counts / repeats

# 이론 분포
k = np.arange(0, n+1)
theo = binom.pmf(k, n, p)

fig = go.Figure()
fig.add_bar(x=vals, y=emp_prob, name="시뮬레이션", opacity=0.7)
fig.add_scatter(x=k, y=theo, mode="lines+markers", name="이론(이항분포)", line=dict(width=2))
fig.update_layout(
    title=f"이항분포 비교 (n={n}, p={p:.3f})",
    xaxis_title="성공 횟수",
    yaxis_title="확률",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("**포인트**: 시행 수가 커질수록 시뮬레이션 막대와 이론 곡선이 점점 가까워집니다 (대수의 법칙).")

with st.expander("📎 시뮬레이션 원자료 보기"):
    st.dataframe(
        px.data.tips() if False else
        {"성공횟수": sim[: min(1000, repeats)]}  # 큰 데이터 테이블 렌더링 부담 줄이기
    )
