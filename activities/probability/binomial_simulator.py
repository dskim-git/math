import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom

# --- utils가 있으면 사용, 없으면 안전한 대체 함수 사용 ---
try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(title: str, subtitle: str = "", icon: str = "📊"):
        st.markdown(f"### {icon} {title}")
        if subtitle:
            st.caption(subtitle)
    def anchor(name: str = "content"):
        st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name: str = "content"):
        components.html(f"<script>window.location.hash = '{name}'</script>", height=0)

META = {
    "title": "확률 시뮬레이터 (이항분포 비교)",
    "description": "베르누이/동전/주사위 실험을 반복 시뮬레이션하고 이론 이항분포와 비교합니다.",
}

def render():
    # ✅ 제목은 여기에서만 1번 출력
    page_header("확률 시뮬레이터", "베르누이/동전/주사위 실험과 이론 분포 비교", icon="📊")

    # ----- 사이드바: 폼으로 묶어서 조작 시 rerun 방지 -----
    with st.sidebar.form("binom_form", clear_on_submit=False):
        st.subheader("⚙️ 실험 설정")
        mode = st.selectbox("실험 종류", ["동전 던지기(공정)", "주사위(특정 눈)", "일반 베르누이(p)"])
        n = st.slider("1회 실험 시행 수 (n)", 1, 200, 30)
        repeats = st.slider("반복 횟수 (시뮬레이션 반복)", 100, 20000, 3000, step=100)

        face = 6  # 기본값
        if mode == "주사위(특정 눈)":
            face = st.number_input("성공 눈 (1~6)", min_value=1, max_value=6, value=6, step=1)

        submitted = st.form_submit_button("적용하기", use_container_width=True)

    # ----- 폼 읽기 및 파라미터 해석 -----
    if mode == "동전 던지기(공정)":
        p = 0.5
        label = "앞면(성공)"
    elif mode == "주사위(특정 눈)":
        p = 1/6
        label = f"{face} 눈"
    else:
        # 일반 베르누이: p는 본문에서 입력받도록(슬라이더가 폼 안에 있으면 괜찮지만, 시각적으로 분리 가능)
        # 폼 rerun을 줄이려면 이 값도 폼 안에 넣어도 됩니다. 여기서는 본문에 위치.
        p = st.slider("성공확률 p", 0.0, 1.0, 0.35, 0.01, key="p_slider_main")
        label = "성공"

    st.write(f"**성공 조건:** {label} | **성공확률 p:** {p:.3f}")

    # ----- 그래프 위치 앵커(렌더 위쪽에 설치) -----
    anchor("graph")

    # ----- 시뮬레이션 -----
    rng = np.random.default_rng()
    sim = rng.binomial(n=n, p=p, size=repeats)

    counts = np.bincount(sim, minlength=n+1)
    k_emp = np.nonzero(counts)[0]
    emp_prob = counts[counts > 0] / repeats

    k = np.arange(0, n+1)
    theo = binom.pmf(k, n, p)

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
        st.dataframe({"성공횟수": sim[: min(1000, repeats)]})

    # ----- 폼 제출 직후엔 그래프 위치로 복귀 -----
    if submitted:
        scroll_to("graph")
