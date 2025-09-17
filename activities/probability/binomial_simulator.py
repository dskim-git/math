import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px  # (원 코드 호환용; 실제 사용 안 해도 무방)
from scipy.stats import binom

# --- utils가 있으면 사용, 없으면 안전한 대체 함수 사용 ---
try:
    from utils import set_base_page, page_header
except Exception:
    def set_base_page(title: str, icon: str = "📊"):
        # home.py에서 set_page_config를 이미 했으므로 여기선 간단 표시만
        st.markdown(f"### {icon} {title}")

    def page_header(title: str, subtitle: str = ""):
        st.header(title)
        if subtitle:
            st.caption(subtitle)

META = {
    "title": "확률 시뮬레이터 (이항분포 비교)",
    "description": "베르누이/동전/주사위 실험을 반복 시뮬레이션하고 이론 이항분포와 비교합니다.",
}

def render():
    set_base_page("확률 시뮬레이터", "📊")
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교")

    st.sidebar.subheader("⚙️ 실험 설정")
    mode = st.sidebar.selectbox(
        "실험 종류",
        ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"]
    )
    n = st.sidebar.slider("1회 실험 시행 수 (n)", 1, 200, 30)
    repeats = st.sidebar.slider("반복 횟수 (시뮬레이션 반복)", 100, 20000, 3000, step=100)

    if mode == "동전 던지기(공정)":
        p = 0.5
        label = "앞면(성공)"
    elif mode == "주사위(특정 눈)":
        face = st.sidebar.number_input("성공 눈 (1~6)", min_value=1, max_value=6, value=6, step=1)
        p = 1/6  # 공정 주사위에서 특정 눈이 나올 확률
        label = f"{face} 눈"
    else:
        p = st.sidebar.slider("성공확률 p", 0.0, 1.0, 0.35, 0.01)
        label = "성공"

    st.write(f"**성공 조건:** {label} | **성공확률 p:** {p:.3f}")

    # --- 시뮬레이션 ---
    rng = np.random.default_rng()
    # (repeats,) 크기의 배열: 각 반복에서 n회 베르누이 시행 성공 개수
    sim = rng.binomial(n=n, p=p, size=repeats)

    # 경험적 분포 (성공 횟수별 상대도수)
    # np.bincount가 빠르고 간단합니다.
    counts = np.bincount(sim, minlength=n+1)
    k_emp = np.nonzero(counts)[0]
    emp_prob = counts[counts > 0] / repeats

    # 이론 분포 (이항분포 pmf)
    k = np.arange(0, n+1)
    theo = binom.pmf(k, n, p)

    # --- 시각화 ---
    fig = go.Figure()
    fig.add_bar(x=k_emp, y=emp_prob, name="시뮬레이션", opacity=0.7)
    fig.add_scatter(x=k, y=theo, mode="lines+markers", name="이론(이항분포)", line=dict(width=2))
    fig.update_layout(
        title=f"이항분포 비교 (n={n}, p={p:.3f})",
        xaxis_title="성공 횟수",
        yaxis_title="확률",
        legend_title="범례",
        bargap=0.05,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**포인트**: 시행 수가 커질수록 시뮬레이션 막대와 이론 곡선이 점점 가까워집니다 (대수의 법칙).")

    with st.expander("📎 시뮬레이션 원자료 보기"):
        # 큰 테이블 렌더링 부담을 줄이기 위해 앞부분만 미리보기
        st.dataframe({"성공횟수": sim[: min(1000, repeats)]})
