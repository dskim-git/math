import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from utils import set_base_page, page_header

set_base_page("선형회귀 직선맞춤", "📈")
page_header("선형회귀 직선맞춤", "업로드/생성 데이터에 직선 적합 & R²")

st.sidebar.subheader("⚙️ 데이터 준비")
data_mode = st.sidebar.radio("데이터 선택", ["직접 업로드", "임의 데이터 생성"], horizontal=True)

if data_mode == "직접 업로드":
    up = st.file_uploader("CSV 업로드 (열 이름: x, y)", type=["csv"])
    if up is not None:
        df = pd.read_csv(up)
    else:
        st.stop()
else:
    n = st.sidebar.slider("표본 개수", 10, 2000, 200)
    slope = st.sidebar.number_input("기울기(β1)", value=2.0)
    intercept = st.sidebar.number_input("절편(β0)", value=1.0)
    noise = st.sidebar.number_input("잡음 표준편차", value=3.0, min_value=0.0)
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, n)
    y = intercept + slope * x + rng.normal(0, noise, size=n)
    df = pd.DataFrame({"x": x, "y": y})

st.write("데이터 미리보기", df.head())

X = df[["x"]].values
y = df["y"].values
model = LinearRegression().fit(X, y)
beta0 = model.intercept_
beta1 = model.coef_[0]
r2 = model.score(X, y)

st.metric("적합식", f"ŷ = {beta0:.3f} + {beta1:.3f}x")
st.metric("결정계수 R²", f"{r2:.4f}")

x_line = np.linspace(df["x"].min(), df["x"].max(), 200)
y_line = beta0 + beta1 * x_line

fig = go.Figure()
fig.add_scatter(x=df["x"], y=df["y"], mode="markers", name="데이터", opacity=0.7)
fig.add_scatter(x=x_line, y=y_line, mode="lines", name="적합직선", line=dict(width=3))
fig.update_layout(title="선형회귀 직선 적합", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig, use_container_width=True)
